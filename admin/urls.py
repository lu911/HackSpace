from django.conf.urls.defaults import patterns, url
from views import ShowSolveStatusView, ShowSolverStatusView, SearchUserView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^status/', ShowSolveStatusView),
    url(r'^solver/(\w+)/', ShowSolverStatusView),
    url(r'^user/', SearchUserView),
)
