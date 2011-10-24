# Create your views here.
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

from forms import VoteForm

def do_vote(keyword, poll_pk):
	return False

def vote(request, pk):
	c = {}
	c.update(csrf(request))
	if request.method == 'POST':
		form = VoteForm(request.POST)
		if form.is_valid():
			if do_vote(form.clean_keyword(),pk):
				return HttpResponseRedirect('/TODO-success/')
	else:
		form = VoteForm(initial={'poll_id':pk})

	c['form'] = form
	return render_to_response('vote.html', c)

