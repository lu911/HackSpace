#-*-coding:utf-8-*-
from models import Board, Category
from forms import PostForm, AdminPostForm

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

def WritePostView(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            form = AdminPostForm(request.POST)
        else:
            form = PostForm(request.POST)
        if form.is_valid():
            post = Board(user=request.user,
                         category=form.cleaned_data['category'],
                         title=form.cleaned_data['title'],
                         content=form.cleaned_data['content'])
            post.save()
            return HttpResponseRedirect('/board/')
    else:
        if request.user.is_superuser:
            form = AdminPostForm(request.POST)
        else:
            form = PostForm(initial=request.GET)
    return render(request, 'board/write_post.html', dict(form=form))

def ShowPostListView(request):
    posts = Board.objects.order_by('category', '-time')
    return render(request, 'board/render_post_list.html', dict(posts=posts))

def ShowPostContentView(request, post_id):
    try:
        post = Board.objects.get(id=post_id)
        if post.user.id == request.user.id:
            is_author = True
        else:
            is_author = False
        return render(request, 'board/render_post_content.html', dict(post=post, is_author=is_author))
    except Board.DoesNotExist:
        return HttpResponseRedirect('/board/')

def ModifyPostView(request, post_id):
    try:
        post = Board.objects.get(id=post_id, user=request.user)
        default = {
            'category' : post.category,
            'title' : post.title,
            'content' : post.content
        }
        if request.method == 'POST':
            if request.user.is_superuser:
                form = AdminPostForm(request.POST)
            else:
                form = PostForm(request.POST)
            if form.is_valid():
                post.category = form.cleaned_data['category']
                post.title = form.cleaned_data['title']
                post.content = form.cleaned_data['content']
                post.save()
                return HttpResponseRedirect('/board/show-post/%s' % post_id)
        else:
            if request.user.is_superuser:
                form = AdminPostForm(initial=default)
            else:
                form = PostForm(initial=default)
        return render(request, 'board/write_post.html', dict(form=form))
    except Board.DoesNotExist:
        return HttpResponseRedirect('/board/show-post/%s' % post_id)
    return HttpResponseRedirect('/board/')

def DeletePostView(request, post_id):
    try:
        post = Board.objects.get(id=post_id, user=request.user)
        post.delete()
        return HttpResponseRedirect('/board/')
    except Board.DoesNotExist:
        if request.user.is_superuser:
            post = Board.objects.get(id=post_id)
            post.delete()
            return HttpResponseRedirect('/board/')
        else:
            return HttpResponseRedirect('/board/show-post/%s' % post_id)
