#-*-coding:utf-8-*-
from models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#@login_required(login_url='/login/')
def ProbListView(request):
    tagName = request.GET.get('tag')
    #tag_id = TagName.objects.get(tag=tagName)
    #tag_list = TagName.objects.all()
    #probIds = []
    probIds = ProbTag.get_from_prob(1)
    print probIds
    #prob_list = Problem.objects.get(
    return render(request,'challenge/list.html')


