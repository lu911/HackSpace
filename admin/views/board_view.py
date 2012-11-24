#-*-coding:utf-8-*-
from django.shortcuts import render
from board.models import Category, Board
from admin.forms import CategoryForm

def AdminAddBoardCategoryView(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            if request.user.is_superuser:
                Category.objects.create(category_name=form.cleaned_data['category_name'])
    else:
        form = CategoryForm(initial=request.GET)
    return render(request, 'admin/board/category_add.html', dict(form=form, categories=categories))

def AdminModifyBoardCategoryView(request, category_id):
    if request.user.is_superuser:
        try:
            category = Category.objects.get(id=category_id)
            default = {
                'category' : category.name
            }
            if request.method == 'POST':
                form = CategoryForm(request.POST)
                if form.is_valid():
                    category.name = category_name
                    category.save()
            else:
                form = CategoryForm(initial=default)
        except:
            form = CategoryForm(initial=request.GET)
    return render(request, 'admin/board/category_modify.html', dict(form=form))

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
    return HttpResponseRedirect('/admin/board/')


