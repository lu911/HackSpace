from django.conf.urls import patterns, include, url
from django.shortcuts import render
import os

from member.views import * 
from challenge.views import *
from admin.views import *
from rank.views import ShowRankView, ShowRankGraphView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', lambda request:render(request, 'index.html')),

    url(r'^register/', memberRegisterView),
    url(r'^login/', memberLoginView),
    url(r'^logout/', memberLogout),

    url(r'^challenge/$', ProbListView),
    url(r'^challenge/auth/',ChallengeAuthView),

    url(r'^rank/', ShowRankView),
    url(r'^rank2/', ShowRankGraphView),

    url(r'^admin/', include('admin.urls')),
    url(r'^board/', include('board.urls')),

    url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': 'static'}),
    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'uploads'})
)
