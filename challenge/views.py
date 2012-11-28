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
        auth = request.POST.get('auth')
        print auth
    except:
        pass
    print 'test'
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
    try:
        # Check Problem for auth
        prob = Problem.objects.get(prob_auth=auth)
    except Problem.DoesNotExist:
        return render(request, 'challenge/list.html', dict(fail=True))

    try:
        # Check Problem was solved
        authLog = AuthLog.objects.get(user_id=request.user, prob_id=prob, auth_type=1)
        return render(request, 'challenge/list.html', dict(solved=True))
    except:
        if prob.prob_auth == auth:
            authType = 1
            # UserProfile Save
            user = request.user.get_profile()
            user.score += prob.prob_point
            last_solve_time = datetime.datetime.now()
            user.save()
            # Problem Data Save
            prob.prob_solver += 1
            prob.save()
        else:
            authType = 0
        # Input authentication data in Authlog Database
        authLog = AuthLog(prob_id=prob, user_id=request.user,
                          auth_type=authType, auth_time=datetime.datetime.now(),
                          auth_ip=request.META['REMOTE_ADDR'], auth_value=auth)
        authLog.save()
    return render(request, 'challenge/list.html', dict(solve=True))
