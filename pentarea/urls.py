from django.conf.urls.defaults import * 
from member.views import * 

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
<<<<<<< HEAD
    (r'^register/$', memberRegisterView),
    (r'^login/$', memberLoginView),
    (r'^logout/$', memberLogout),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/wisedier/git/pentarea/static'})
=======
    (r'^register/', MemberRegisterView),
    (r'^login/', MemberLoginView),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'})
    #(r'^css/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': css }),
    #(r'^js/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': js }),
    #(r'^img/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': img })
>>>>>>> e097d3522b861cb2420e52e93cc764f995ef689e
    # Examples:
    # url(r'^$', 'pentarea.views.home', name='home'),
    # url(r'^pentarea/', include('pentarea.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
