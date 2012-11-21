from django.conf.urls.defaults import patterns, url
from views import *
from django.shortcuts import render

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ShowSolveStatusView),
    url(r'^solver/(\w+)/', ShowSolverStatusView),
    url(r'^user/', SearchUserView),

    url(r'^challenge/', AdminChallengeManagerView),
    
    url(r'^add-tag/', AdminAddTagManagerView),
    url(r'^check-tag/', AdminTagCheckView),
    url(r'^modify-tag/', AdminModifyTagView),
    url(r'^delete-tag/', AdminDeleteTagView),
    
    url(r'^add-prob/', AdminAddProblemManagerView),
    url(r'^modify-prob/', AdminModifyProblemView),
    url(r'^delete-prob/', AdminDeleteProblemView),
    url(r'^problist/', AdminProblemListManagerView),
)
