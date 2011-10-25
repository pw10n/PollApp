# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.template import RequestContext

from forms import VoteForm, ConfirmForm

from models import *

import re, base64


### Vote Views ###

def vote(request, pk):
	request.session.set_test_cookie()
	c = {}
	poll = get_object_or_404(Poll, pk=pk)
	
	c.update(csrf(request))
	sid = request.session.session_key
	if request.method == 'POST':
		form = VoteForm(request.POST)
		if form.is_valid():
			keyword = form.clean_keyword()
			choice = poll.choiceByKeyword(keyword=keyword)
			if choice and WebVote.do_vote(sid, choice):
				return HttpResponseRedirect("/success/%s/%s/"%(poll.id,choice.id))
	else:
		form = VoteForm(initial={'poll_id':poll.id,'sid_saved':sid})

	c['form'] = form
	return render_to_response('vote.html', c, context_instance=RequestContext(request))

def confirm(request, poll_pk, keyword):
	request.session.set_test_cookie()
	c = {}
	poll = get_object_or_404(Poll, pk=poll_pk)

	c.update(csrf(request))
	sid = request.session.session_key

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
	return render_to_response('confirm.html', c, context_instance=RequestContext(request))

def verify_auth(auth_header):
	auth_parts = auth_header.split(' ')
	user_pass_parts = base64.b64decode(auth_parts[1]).split(':')
	user_arg = user_pass_parts[0]
	pass_arg = user_pass_parts[1]

	return user_arg == "twilio" and pass_arg == "tw1l10"

@csrf_exempt
def smsVote(request):
	c = {}
	print request.META

	if not 'HTTP_AUTHORIZATION' in request.META or not verify_auth(request.META['HTTP_AUTHORIZATION']):
		res = HttpResponse("Unauthorized")
		res['WWW-Authenticate'] = 'Basic realm="pollapp"'
		res.status_code = 401
		return res

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
				keyword = match.group("keyword")
				if SmsVote.userVotesByPoll(phone, poll):
					c['response'] = "You have already voted in this poll."
				else:
					choice = poll.choiceByKeyword(keyword)
					if not choice:
						c['response'] = "The item you are voting for does not exist."
					else:
						SmsVote.do_vote(phone, choice)
						c['response'] = "You have voted for '%s' in the poll '%s'. Have a good day!" % (poll.title,keyword)

			except ObjectDoesNotExist:
				c['response'] = "Invalid request. (id=1)"

	else:
		print request.method
		raise Http404
	return render_to_response('smstwilio.html', c, context_instance=RequestContext(request))
		
def success(request, poll_pk, choice_pk):
	poll = get_object_or_404(Poll, pk=poll_pk)
	choice = get_object_or_404(Choice, pk=choice_pk)
	return render_to_response('success.html', {'poll':poll,'choice':choice}, context_instance=RequestContext(request))

### Poll Menu ###

@login_required
def poll_view_menu(request):
	pass

### Poll Viewer ###

@login_required
def poll_view(request, poll):
	pass

### Poll Analytics ###

@login_required
def poll_stats(request, poll):
	pass

def cause_an_error(request):
	print poop

