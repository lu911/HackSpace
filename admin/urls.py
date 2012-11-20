from django.conf.urls.defaults import patterns, url
from views import TestView, ShowSolveStatusView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^test/', TestView),
    url(r'^status/', ShowSolveStatusView),
    #(r'^rank/$', lambda request:render(request, 'rank/rank.html')),
)
