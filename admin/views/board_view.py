#-*-coding:utf-8-*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from board.models import Category, Board
from board.forms import AdminPostForm, PostForm
from admin.forms import CategoryForm

@login_required(login_url='/login/')
def AdminWritePostView(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = AdminPostForm(request.POST)
            if form.is_valid():
                post = Board(user=request.user,
                             category=form.cleaned_data['category'],
                             title=form.cleaned_data['title'],
                             content=form.cleaned_data['content'])
                post.save()
                return HttpResponseRedirect('/admin/add-category/')
        else:
            form = AdminPostForm(initial=request.GET)
        return render(request, 'board/write_post.html', dict(form=form))
    else:
        form = PostForm(initial=request.GET)
        return render(request, 'board/write_post.html', dict(form=form))

@login_required(login_url='/login/')
def AdminAddBoardCategoryView(request):
    if request.user.is_superuser:
        categories = Category.objects.all()
        posts = Board.objects.order_by('-time')[:10]
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                Category.objects.create(name=form.cleaned_data['category_name'])
        else:
            form = CategoryForm(initial=request.GET)
        return render(request, 'admin/board/category_add.html', dict(form=form,
                                                                     categories=categories,
                                                                     posts=posts))
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def AdminModifyBoardCategoryView(request, category_id):
    if request.user.is_superuser:
        categories = Category.objects.all()
        posts = Board.objects.order_by('-time')[:10]
        try:
            category = Category.objects.get(id=category_id)
            default = {
                'category_name' : category.name
            }
            if request.method == 'POST':
                form = CategoryForm(request.POST)
                if form.is_valid():
                    category.name = form.cleaned_data['category_name']
                    category.save()
                    return HttpResponseRedirect('/admin/add-category/')
            else:
                form = CategoryForm(initial=default)
                return render(request, 'admin/board/category_modify.html', dict(form=form,
                                                                                categories=categories,
                                                                                category_id=category_id,
                                                                                posts=posts))
        except:
            return HttpResponseRedirect('/admin/add-category/')
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def AdminDeleteBoardCategoryView(request, category_id):
    if request.user.is_superuser:
        try:
            category = Category.objects.get(id=category_id)
            posts = Board.objects.filter(category_id=category_id)
            etc_category = Category.objects.get(id=1)
            for post in posts:
                post.category_id = etc_category
                post.save()
            category.delete()
        except Category.DoesNotExist:
            pass
        return HttpResponseRedirect('/admin/add-category/')
    else:
        return HttpResponseRedirect('/')
