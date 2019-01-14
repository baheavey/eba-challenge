from django.shortcuts import render
from django.http import HttpResponse
import datetime
from .models import ScoringCategory, ScoringFrequency, ScoringItem, Scorecard, Challenge, Team, User, PointTracking
#from django.views.decorators.clickjacking import xframe_options_exempt

# handle scoring for one-time items appropriately

#@xframe_options_exempt
def daily_tracker(request, challenge_id, email, offset=0):
	
	# Find Challenge
	try:
		#challenge = Challenge.objects.get(id=1)
		challenge = Challenge.objects.get(id=challenge_id)
		scorecard = challenge.scorecard
		challenge_start_date = challenge.start_date
		challenge_stop_date  = challenge.stop_date
	except Challenge.DoesNotExist:
		return render(request, 'scorecard.html', {'error': "Error: Unknown Challenge"})

	# Find User
	try:
		user = User.objects.get(email__iexact=email) # __iexact makes the email address lookup case insensitive
	except User.DoesNotExist:
		return render(request, 'scorecard.html', {'error': "Error: No Such User"})

	# Calculate Dates
	today = datetime.datetime.today()
	weekday = today.weekday() #returns 0 for monday... 6 for sunday
	week_start_date = today - datetime.timedelta(days=weekday)
	week_stop_date  = today + datetime.timedelta(days=(6-weekday))
	display_date = today.date() + datetime.timedelta(days=offset)
	
	# Build Next & Previous URLs
	current_url = request.get_full_path()
	if display_date <= challenge_start_date:
		display_date = challenge_start_date
		offset = (challenge_start_date - today.date()).days
		prev_url = ""
		next_url = current_url.rsplit('/',1)[0] + '/' + str(offset + 1)
	elif display_date >= challenge_stop_date:
		display_date = challenge_stop_date
		offset = (challenge_stop_date - today.date()).days
		next_url = ""
		prev_url = current_url.rsplit('/',1)[0] + '/' + str(offset - 1)
	else:
		prev_url = current_url.rsplit('/',1)[0] + '/' + str(offset - 1)
		next_url = current_url.rsplit('/',1)[0] + '/' + str(offset + 1)

	# Should data entry be disabled?
	entry_days = 2
	if offset <= 0 and offset > -entry_days:
		form_disabled = False
	else:
		form_disabled = True

	# Get all scorecard items
	scorecard_items = scorecard.item.all().order_by("category")
	points = PointTracking.objects.filter(user=user, challenge=challenge)

	# If submit button pushed and within date range for editting
	post = ""
	if request.POST:
		if not form_disabled:
			post = update_points(request.POST, scorecard_items, points, display_date, user, challenge)
			# Updated points after records reflect latest entry
			points = PointTracking.objects.filter(user=user, challenge=challenge)
		else:
			return render(request, 'scorecard.html', {'error': "Error: You Can't Submit Points For This Day"})
	
	challenge_score = 0
	weekly_score = 0
	date_view_points = []
	bonuses = []
	
	for point in points:
		challenge_score += point.score
		# .date() converts datetime type to date type
		if point.record_date >= week_start_date.date() and point.record_date <= week_stop_date.date():
			weekly_score += point.score
		if point.record_date == display_date:
			date_view_points.append(point)
		if point.item.category.name == "Bonus":
			bonuses.append(point.item.name)
		
	return render(request, 'scorecard.html', {'scorecard': scorecard, 'scorecard_items': scorecard_items, 'points': points, 'challenge_score': challenge_score, 'weekly_score': weekly_score, 'date_view_points': date_view_points, 'display_date': display_date, 'challenge_start_date': challenge_start_date, 'challenge_stop_date': challenge_stop_date, 'next_url': next_url, 'prev_url': prev_url, 'offset': offset, 'form_disabled': form_disabled, 'bonuses': bonuses})
		
#@xframe_options_exempt		
def update_points(post_data, scorecard_items, points, display_date, user, challenge):
	# All points currently registered for display day
	display_day_points = points.filter(record_date=display_date)
	# Loop through all items in scorecard for this challenge
	for item in scorecard_items:
		
		# If this item is in the current form
		if str(item.id) in post_data:
			
			# See if preexisting point for this item is available
			try:
				point = display_day_points.get(item=item.id)
			except PointTracking.DoesNotExist:
				point = ''
			
			# All form items submitted with non empty value that corespond to a tracking item on scorecard		
			if post_data[str(item.id)]:

				# Making sure submitted score is an int
				try:
					score = int(post_data[str(item.id)])
				except ValueError:
					score = 0
				# Making sure the int is in range for this particular item
				if score > item.max_points or score < item.min_points:
					score = item.min_points
			
				# If a record already exists for this item on this day, update its score
				if point:
					point.score = score
					point.save()
				# If no record exists for this item on this day, create a new entry
				else:
					PointTracking.objects.create(record_date=display_date, item=item, user=user, challenge=challenge, score=int(post_data[str(item.id)]))
			
			# If an entry for an existing point was cleared in the form field, convert to 0
			elif point:
				point.score = 0
				point.save()
	