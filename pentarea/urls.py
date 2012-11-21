from django.conf.urls import patterns, include, url
from django.shortcuts import *
from member.views import * 
from challenge.views import *
from admin.views import *
from rank.views import ShowRankView
from django.shortcuts import render

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^register/', memberRegisterView),
    url(r'^login/', memberLoginView),
    url(r'^logout/', memberLogout),
    
    url(r'^admin/tag/', AdminTagManagerView),
    url(r'^admin/prob/', AdminProblemManagerView),
    url(r'^admin/modify-prob/', AdminModifyProblemView),
    
    
    url(r'^challenge/', ProbListView),
    url(r'^challenge/auth/', AuthView),
    
    
    url(r'^rank/', ShowRankView),
    
    
    #url(r'^rank/$', lambda request:render(request, 'rank/rank.html')),
    url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': 'static'}),
    url(r'^board/', lambda request:render(request, 'board/board.html')),
    url(r'^admin/', include('admin.urls')),
)
