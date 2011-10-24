from pollapp.models import * 
from django.contrib import admin

class ChoiceInline(admin.StackedInline):
	model = Choice
	extra = 0

class PollAdmin(admin.ModelAdmin):
	inlines = [ChoiceInline]
	list_display = ('title', 'inactive')

admin.site.register(Poll, PollAdmin)
admin.site.register(SmsVote)
admin.site.register(WebVote)

