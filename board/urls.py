from django.conf.urls import patterns, url
from views import ShowPostListView, ShowPostOfCategoryListView, WritePostView, ShowPostContentView, ModifyPostView, DeletePostView

urlpatterns = patterns('',
    url(r'^$', ShowPostListView),
    url(r'^(\w+)/$', ShowPostOfCategoryListView),
    url(r'^write-post/', WritePostView),
    url(r'^show-post/(\w+)/', ShowPostContentView),

    url(r'^modify-post/(\w+)/', ModifyPostView),
    url(r'^delete-post/(\w+)/', DeletePostView),
)
