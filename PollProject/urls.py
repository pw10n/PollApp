from django.conf.urls.defaults import patterns, include, url

from pollapp.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PollProject.views.home', name='home'),
    # url(r'^PollProject/', include('PollProject.foo.urls')),

		(r'^$', vote_generic),
		(r'^vote/(?P<pk>\d+)/$', vote),	
		(r'^vote/(?P<poll_pk>\d+)(/|\.)(?P<keyword>\w+)/$', confirm),
		(r'^sms/$',smsVote),
		(r'^success/(?P<poll_pk>\d+)/(?P<choice_pk>\d+)/$', success),
		(r'^cause_an_error/$', cause_an_error),
		(r'^polls/$', poll_menu),
		(r'^polls/view/(?P<poll_pk>\d+)/$', poll_view),
		(r'^polls/view/(?P<poll_pk>\d+)/choice/(?P<keyword>\w+)/$', choice_view),
		(r'^polls/view/(?P<poll_pk>\d+)/stat/$', poll_stats),

		(r'^accounts/login/$', 'django.contrib.auth.views.login'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

