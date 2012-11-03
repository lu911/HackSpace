#-*-coding:utf-8-*-
from models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
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
            raise ValueError
    except ValueError:
        probData=ProbTag.get_from_all_prob()
    return render(request,'challenge/list.html',dict(tag_list=tagList, prob_data=probData))

def AuthView(request):
    auth=request.POST.get('auth')
#    prob_id=request.POST.get('prob_id')
    try:
        prob=Problem.objects.get(prob_auth=auth)
        if prob.prob_flag == 1:
            result='already cleared'
        else:
            result='OK'
            prob.prob_flag=1
            prob.save()
    except:
        result='fail'
    return HttpResponse(json.dumps(dict(auth=result)))
