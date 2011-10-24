from django.core.exceptions import ObjectDoesNotExist
from django import forms
from models import *

class VoteForm(forms.Form):
	sid_saved = forms.CharField(widget=forms.HiddenInput())
	poll_id = forms.IntegerField(widget=forms.HiddenInput())
	keyword = forms.CharField(max_length=20)

	def clean_keyword(self):
		sid = self.cleaned_data['sid_saved']
		poll_id = self.cleaned_data['poll_id']
		data = self.cleaned_data['keyword']

		try:
			poll = Poll.objects.get(id=poll_id)
			if WebVote.userVotesByPoll(sid,poll):
				raise forms.ValidationError("You have already voted in this poll.")
			if not poll.choiceByKeyword(data):
				raise forms.ValidationError("The keyword '%s' does not exist in poll!" % data)
		except ObjectDoesNotExist:
			raise forms.ValidationError("Poll does not exist")

		return data 

class ConfirmForm(forms.Form):
	sid_saved = forms.CharField(widget=forms.HiddenInput())
	poll_id = forms.IntegerField(widget=forms.HiddenInput())
	keyword = forms.CharField(max_length=20,widget=forms.HiddenInput())

	def clean_keyword(self):
		sid = self.cleaned_data['sid_saved']
		poll_id = self.cleaned_data['poll_id']
		data = self.cleaned_data['keyword']

		try:
			poll = Poll.objects.get(id=poll_id)
			if WebVote.userVotesByPoll(sid,poll):
				raise forms.ValidationError("You have already voted in this poll.")
			if not poll.choiceByKeyword(data):
				raise forms.ValidationError("The keyword '%s' does not exist in poll!" % data)
		except ObjectDoesNotExist:
			raise forms.ValidationError("Invalid vote! (Poll or choice does not exist)")

		return data 

