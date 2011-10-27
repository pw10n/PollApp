from django.core.exceptions import ObjectDoesNotExist
from django import forms
from models import *
import re

class VoteForm(forms.Form):
	sid_saved = forms.CharField(widget=forms.HiddenInput())
	poll_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
	keyword = forms.CharField(max_length=20)

	def clean_keyword(self):
		sid = self.cleaned_data['sid_saved']
		poll_id = None 
		if 'poll_id' in self.cleaned_data:
			poll_id = self.cleaned_data['poll_id']
		data = self.cleaned_data['keyword']
		keyword = data

		# if no poll_id is passed, we need to be able to find it in keyword
		if poll_id == None:
			match_strict = re.match("(?P<poll_pk>\d+)\.(?P<keyword>\w+)", data)
			if match_strict:
				poll_id = match_strict.group("poll_pk") 
				if len(Poll.objects.filter(id=poll_id)) == 0:
					raise forms.ValidationError("Poll does not exist!")
			else:
				raise forms.ValidationError("Invalid keyword! Missing poll prefix.")

		match = re.match("((?P<poll_pk>\d+)\.)?(?P<keyword>\w+)", data)
		if match:
			keyword = match.group("keyword")

		try:
			poll = Poll.objects.get(id=poll_id)
			if WebVote.userVotesByPoll(sid,poll):
				raise forms.ValidationError("You have already voted in this poll.")
			if not poll.choiceByKeyword(keyword):
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

