from django.conf.urls.defaults import patterns, url
from views import MainView, ShowSolveStatusView, ShowSolverStatusView, SearchUserView, AdminTagManagerView, AdminTagCheckView, AdminModifyTagView, AdminDeleteTagView, AdminProblemManagerView, AdminModifyProblemView
from django.shortcuts import render

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', MainView),

    url(r'^status/', ShowSolveStatusView),
    url(r'^solver/(\w+)/', ShowSolverStatusView),
    url(r'^user/', SearchUserView),

    url(r'^tag/', AdminTagManagerView),
    url(r'^check-tag/', AdminTagCheckView),
    url(r'^modify-tag/', AdminModifyTagView),
    url(r'^delete-tag/', AdminDeleteTagView),
    
    url(r'^prob/', AdminProblemManagerView),
    url(r'^modify-prob/', AdminModifyProblemView),
)
