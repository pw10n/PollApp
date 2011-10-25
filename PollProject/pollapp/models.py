from django.db import models

# Create your models here.

import datetime

class Poll(models.Model):
	title = models.CharField(max_length=200)
	inactive = models.BooleanField()

	def choiceByKeyword(self, keyword):
		choices = Choice.objects.filter(poll=self)
		found = None
		for choice in choices:
			if choice.keyword == keyword:
				found = choice 
		return found

	def __unicode__(self):
		return self.title

class Choice(models.Model):
	keyword = models.CharField(max_length=20)
	description = models.CharField(max_length=200)
	poll = models.ForeignKey('Poll')

	def __unicode__(self):
		return self.keyword

class Vote(models.Model):
	timestamp = models.DateTimeField('timestamp')
	choice = models.ForeignKey('Choice')

	class Meta:
		abstract = True

class SmsVote(Vote):
	phone_number = models.CharField(max_length=25)

	@staticmethod
	def userVotesByPoll(phone_number, poll):
		poll_choices = Choice.objects.filter(poll=poll)
		smsvotes = SmsVote.objects.all()
		smsvotes_in_poll_by_sid = []
		for smsvote in smsvotes:
			if smsvote.choice in poll_choices and smsvote.phone_number == phone_number:
				smsvotes_in_poll_by_sid += [smsvote]
		return smsvotes_in_poll_by_sid

	@staticmethod
	def do_vote(phone_number, choice):
		vote = SmsVote()
		vote.choice = choice
		vote.phone_number = phone_number
		vote.timestamp = datetime.datetime.now()
		vote.save()

		return vote

	def __unicode__(self):
		return "SmsVote: %s (%s) " % (self.choice.keyword, self.phone_number)

class WebVote(Vote):
	session_id = models.CharField(max_length=200)

	@staticmethod
	def userVotesByPoll(sid, poll):
		poll_choices = Choice.objects.filter(poll=poll)
		webvotes = WebVote.objects.all()
		webvotes_in_poll_by_sid = []
		for webvote in webvotes:
			if webvote.choice in poll_choices and webvote.session_id == sid:
				webvotes_in_poll_by_sid += [webvote]
		return webvotes_in_poll_by_sid

	# This method does not prevent a user from voting more than once, 
	# please call userVotesByPoll to verify that the user has not
	# already voted.
	@staticmethod
	def do_vote(sid, choice):
		vote = WebVote()
		vote.choice = choice
		vote.session_id = sid
		vote.timestamp = datetime.datetime.now()
		vote.save()

		return vote
	
	def __unicode__(self):
		return "WebVote: %s (%s)" % (self.choice.keyword, self.session_id)

