from django.conf.urls import patterns, include, url
from django.shortcuts import render

from member.views import * 
from challenge.views import *
from admin.views import *
from rank.views import ShowRankView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^register/', memberRegisterView),
    url(r'^login/', memberLoginView),
    url(r'^logout/', memberLogout),

    url(r'^challenge/$', ProbListView),
    url(r'^challenge/auth/',ChallengeAuthView),


    url(r'^rank/', ShowRankView),


    url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': 'static'}),
    url(r'^admin/', include('admin.urls')),

    # test page
    url(r'^board/', lambda request:render(request, 'board/board.html')),
)
