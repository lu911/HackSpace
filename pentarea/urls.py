from django.conf.urls.defaults import * 
from django.shortcuts import *
from member.views import * 
from challenge.views import *
from rank.views import ShowRankView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    (r'^register/$', memberRegisterView),
    (r'^login/$', memberLoginView),
    (r'^logout/$', memberLogout),
    (r'^challenge/$', ProbListView),
    (r'^challenge/auth/$', AuthView),
    (r'^rank/$', ShowRankView),
    #(r'^rank/$', lambda request:render(request, 'rank/rank.html')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'})
    # Examples:
    # url(r'^$', 'pentarea.views.home', name='home'),
    # url(r'^pentarea/', include('pentarea.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
