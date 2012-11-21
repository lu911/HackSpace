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
    
    url(r'^admin/tag/', AdminTagManagerView),
    url(r'^admin/check-tag/', AdminTagCheckView),
    url(r'^admin/modify-tag/', AdminModifyTagView),
    url(r'^admin/delete-tag/', AdminDeleteTagView),
    
    url(r'^admin/prob/', AdminProblemManagerView),
    url(r'^admin/modify-prob/', AdminModifyProblemView),
    url(r'^admin/delete-prob/', AdminDeleteProblemView),
    url(r'^admin/problist/', AdminProblemListManagerView),
    
    url(r'^challenge/$', ProbListView),
    url(r'^challenge/auth/',ChallengeAuthView),
    
    
    url(r'^rank/', ShowRankView),
    
    
    #url(r'^rank/$', lambda request:render(request, 'rank/rank.html')),
    url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': 'static'}),
    url(r'^admin/', include('admin.urls')),
    
    # test page
    url(r'^board/', lambda request:render(request, 'board/board.html')),
    url(r'^test1/', lambda request:render(request, 'AwesomeChartJS/demo-animated.html')),
    url(r'^test2/', lambda request:render(request, 'AwesomeChartJS/demo.html')),
    url(r'^test3/', lambda request:render(request, 'AwesomeChartJS/demo-multicolor.html')),
)
