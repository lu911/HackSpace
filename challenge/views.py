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

@login_required(login_url='/login/')
def ChallengeAuthView(request):
    auth = request.POST.get('auth')
    prob_id = request.POST.get('prob-id')
    try:
        prob = Problem.objects.get(id=prob_id)
        authLog = AuthLog.objects.get(user_id=request.user, prob_id=prob, auth_type=1)
        if authLog.count() > 0 :
            reason = "Already Cleared"
        else:
            if prob.prob_auth == auth:
                status = "OK"
                authType = 1
                user = request.user.get_profile()
                user.score += prob.prob_point
                last_solve_time = datetime.datetime.now()
                user.save()
                prob.prob_solver += 1
                prob.save()
            else:
                reason = "Wrong"
                authType = 0
            authLog = AuthLog(prob_id=prob, user_id=request.user, auth_type=authType, auth_time=datetime.datetime.now(), auth_ip=request.META['REMOTE_ADDR'], auth_value=auth)
            authLog.save()
    except Problem.DoesNotExist:
        raise ValidationError("존재 하지 않는 문제입니다.")  
    status = {"status":status, "reason":reason}
    print status
    return HttpResponse(json.dumps(dict(status=status)), mimetype='application/json')
