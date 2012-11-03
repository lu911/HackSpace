#-*-coding:utf-8-*-
from models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#@login_required(login_url='/login/')
def ProbListView(request):
    try:   
        tagID = request.GET.get('tag', None)
        #tag_id = TagName.objects.get(tag=tagName)
        tagList = TagName.objects.all()
        #probIds = []
        if tagID is not None:
            probData = ProbTag.get_from_prob(tagID)
        else:
            probData = ProbTag.get_from_all_prob()
    except:
        probData=ProbTag.get_from_all_prob()
    return render(request,'challenge/list.html',dict(tag_list=tagList, prob_data=probData))
