# Create your views here.
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django import forms

from forms import VoteForm

from models import *

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


def success(request, poll_pk, choice_pk):
	poll = get_object_or_404(Poll, pk=poll_pk)
	choice = get_object_or_404(Choice, pk=choice_pk)
	return render_to_response('success.html', {'poll':poll,'choice':choice})

