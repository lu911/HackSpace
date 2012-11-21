#-*-coding:utf-8-*-
from models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from member.models import UserProfile
from django.http import HttpResponse
import json
import datetime
import time

@login_required(login_url='/login/')
def ProbListView(request):
    try:   
        tagID = request.GET.get('tag', None)
        tagList = TagName.objects.all()
        if tagID is not None:
            probData = ProbTag.get_from_prob(tagID)
        else:
            raise ValueError
    except ValueError:
        probData=ProbTag.get_from_all_prob()
    return render(request,'challenge/list.html',dict(tag_list=tagList, prob_data=probData))

def AuthView(request):
    auth=request.POST.get('auth')
    probId=request.POST.get('prob-id')
    prob=Problem.objects.get(id=probId)
    try:
        authLog=AuthLog.objects.get(user_id=request.user, prob_id=prob, auth_type=1)
    except:
        if(prob.prob_auth == auth):
            result='OK'
            authType=1
            user=UserProfile.objects.get(user=request.user)
            user.score+=prob.prob_point
            last_solve_time=datetime.datetime.now()
            user.save()
            prob.prob_solver += 1
            prob.save()
        else:
            result='fail'
            authType=0
        authLog=AuthLog(prob_id=prob, user_id=request.user, auth_type=authType, auth_time=datetime.datetime.now(), auth_ip=request.META['REMOTE_ADDR'], auth_value=auth)
        authLog.save()
    else:
       result='already cleared'
    return HttpResponse(json.dumps(dict(auth=result)))
