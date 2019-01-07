from django.contrib import admin

# Register your models here.
from .models import ScoringCategory, ScoringFrequency, ScoringItem, Scorecard, Challenge, Team, User, PointTracking

class ScoringItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')

admin.site.register(ScoringCategory)
admin.site.register(ScoringFrequency)
admin.site.register(ScoringItem, ScoringItemAdmin)
admin.site.register(Scorecard)
admin.site.register(Challenge)
admin.site.register(Team)
admin.site.register(User)
admin.site.register(PointTracking)