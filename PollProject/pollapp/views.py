# Create your views here.
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django import forms

from forms import VoteForm, ConfirmForm

from models import *

import re

def vote(request, pk):
	c = {}
	poll = get_object_or_404(Poll, pk=pk)
	
	c.update(csrf(request))
	sid = request.COOKIES['sessionid']
	if request.method == 'POST':
		form = VoteForm(request.POST)
		if form.is_valid():
			keyword = form.clean_keyword()
			choice = get_object_or_404(Choice, keyword=keyword)
			if choice and WebVote.do_vote(sid, choice):
				return HttpResponseRedirect("/success/%s/%s/"%(poll.id,choice.id))
	else:
		form = VoteForm(initial={'poll_id':poll.id,'sid_saved':sid})

	c['form'] = form
	return render_to_response('vote.html', c)

def confirm(request, poll_pk, keyword):
	c = {}
	poll = get_object_or_404(Poll, pk=poll_pk)

	c.update(csrf(request))
	sid = request.COOKIES['sessionid']

	if request.method == 'POST':
		form = ConfirmForm(request.POST)
		if form.is_valid():
		 	keyword = form.clean_keyword()
			choice = get_object_or_404(Choice, keyword=keyword)
			if WebVote.do_vote(sid, choice):
				return HttpResponseRedirect("/success/%s/%s/"%(poll.id, choice.id))
	else:
		form = ConfirmForm(initial={'keyword':keyword,'poll_id':poll.id,'sid_saved':sid})

	c['form'] = form
	c['poll'] = poll
	c['keyword'] = keyword
	return render_to_response('confirm.html', c)

@csrf_exempt
def smsVote(request):
	c = {}
	if request.method == 'POST':
		phone = request.POST['From']
		message = request.POST['Body']
		
		# 1. validate Body, 2. validate has voted, 3. validate choice
		match = re.match("(?P<poll_pk>\d+)\.(?P<keyword>\w+)", message)
		if not match:
			c['response'] = "Invalid request. (id=0)"
		else:
			try:
				poll = Poll.objects.get(id=match.group("poll_pk"))
				if SmsVote.userVotesByPoll(phone, poll):
					c['response'] = "You have already voted in this poll."
				else:
					choice = poll.choiceByKeyword(match.group("keyword"))
					if not choice:
						c['response'] = "The item you are voting for does not exist."
					else:
						SmsVote.do_vote(phone, choice)
						c['response'] = "You have voted for '%s' in the poll '%s'. Have a good day!" % (poll.title,keyword)

			except ObjectNotFound:
				c['response'] = "Invalid request. (id=1)"

	else:
		raise Http404
	return render_to_response('smstwilio.html',c)
		

def success(request, poll_pk, choice_pk):
	poll = get_object_or_404(Poll, pk=poll_pk)
	choice = get_object_or_404(Choice, pk=choice_pk)
	return render_to_response('success.html', {'poll':poll,'choice':choice})

