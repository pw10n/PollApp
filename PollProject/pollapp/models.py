from django.db import models

# Create your models here.

import datetime

class Poll(models.Model):
	title = models.CharField(max_length=200)
	inactive = models.BooleanField()

	def __unicode__(self):
		return self.title

class Choice(models.Model):
	keyword = models.CharField(max_length=20)
	description = models.CharField(max_length=200)

	def __unicode__(self):
		return self.keyword

class Vote(models.Model):
	timestamp = models.DateTimeField('timestamp')

	class Meta:
		abstract = True

class SmsVote(Vote):
	phone_number = models.CharField(max_length=25)

	def __unicode__(self):
		return "SmsVote: " + self.phone_number

class WebVote(Vote):
	voter_id = models.CharField(max_length=200)

	def __unicode__(self):
		return "WebVote: " + self.voter_id

