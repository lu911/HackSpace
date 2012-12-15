#-*-coding:utf-8-*-
from models import Board, Category
from forms import PostForm, AdminPostForm

from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

@login_required(login_url='/login/')
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
            form = AdminPostForm(initial=request.GET)
        else:
            form = PostForm(initial=request.GET)
    return render(request, 'board/write_post.html', dict(form=form))

@login_required(login_url='/login/')
def ShowPostListView(request):
    posts = Board.objects.order_by('category', '-time')
    categories = Category.objects.all()
    return render(request, 'board/board.html', dict(posts=posts,
                                                               categories=categories))

@login_required(login_url='/login/')
def ShowPostOfCategoryListView(request, category_id):
    try:
        categories = Category.objects.all()
        categoryList = []
        for category in categories:
            categoryList.append(category.id)
        selectedCategory = categoryList.index(int(category_id))+1
        posts = Board.objects.filter(category=category_id).order_by('-time')
    except:
        posts = Board.objects.all().order_by('category', '-time')
        categories = Category.objects.all()
        selectedCategory = 0
    return render(request, 'board/board.html', dict(posts=posts,
                                                               categories=categories,
                                                               selectedCategory=selectedCategory))

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
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
