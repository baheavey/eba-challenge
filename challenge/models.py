from django.db import models

class ScoringCategory(models.Model):
	name = models.CharField(max_length=30)
	
	def __str__(self):
		return self.name
		
class ScoringFrequency(models.Model):
	frequency = models.CharField(max_length=30)
	
	def __str__(self):
		return self.frequency

class ScoringItem(models.Model):
	name = models.CharField(max_length=30)
	max_points = models.IntegerField()
	min_points = models.IntegerField()
	frequency = models.ForeignKey(ScoringFrequency, on_delete=models.CASCADE)
	category = models.ForeignKey(ScoringCategory, on_delete=models.CASCADE)
	description = models.CharField(max_length=255, default='')
	
	def __str__(self):
		return self.name

class Scorecard(models.Model):
	name = models.CharField(max_length=30)
	item = models.ManyToManyField(ScoringItem)
	
	def __str__(self):
		return self.name

class Challenge(models.Model):
	name       = models.CharField(max_length=50)
	start_date = models.DateField()
	stop_date  = models.DateField()
	scorecard  = models.ForeignKey(Scorecard, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.name
		
class Team(models.Model):
	name = models.CharField(max_length=30)
	challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
	color = models.CharField(max_length=10)
	
	def __str__(self):
		return self.name

class User(models.Model):
	first_name = models.CharField(max_length=20)
	last_name  = models.CharField(max_length=20)
	email      = models.EmailField()
	team       = models.ManyToManyField(Team)
	#role??, e.g. captain
	
	def __str__(self):
		return u'%s, %s' % (self.last_name, self.first_name)
	
class PointTracking(models.Model):
	record_date = models.DateField()
	item  = models.ForeignKey(ScoringItem, on_delete=models.CASCADE)
	user  = models.ForeignKey(User, on_delete=models.CASCADE)
	challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
	score = models.IntegerField()
	
	def __str__(self):
		return u'%s: %s, %s; item: %s; points: %s' % (self.record_date, self.user.last_name, self.user.first_name, self.item.name, self.score)