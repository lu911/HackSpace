#-*-coding:utf-8-*-
from models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from member.models import UserProfile
from django.http import HttpResponse
from django.core.cache import cache
import json
import datetime
import time

def CheckOnOffLevel(level):
    onOffLevel = cache.get("on_off_level")
    if onOffLevel is None:
        onOffLevel = 0
    if onOffLevel < level:
        return -1
    return onOffLevel
@login_required(login_url='/login/')
def ProbListView(request):
    onOffLevel = CheckOnOffLevel(1)
    if onOffLevel == -1:
        return HttpResponse("This page is closed...")


    try:
        solvedProb = AuthLog.objects.filter(user_id=request.user, auth_type=1)
        solvedProbIds = []
        for prob in solvedProb:
            solvedProbIds.append(prob.prob_id.id)
        solvedProb=True
    except:
        solvedProb=False

    try:
        tagID = request.GET.get('tag', None)
        tagList = TagName.get_from_all_opened_tag()
        if tagID is not None:
            probData = ProbTag.get_from_opened_prob(tagID)
        else:
            raise ValueError
    except ValueError:
        probData=ProbTag.get_from_all_opened_prob()
    return render(request,'challenge/list.html',dict(tag_list=tagList, prob_data=probData,
                                                     solvedProblems=solvedProbIds, solvedProb=solvedProb, onOffLevel = onOffLevel))

@login_required(login_url='/login/')
def ChallengeAuthView(request):
    if CheckOnOffLevel(2) == -1:
        return HttpResponse("This page is closed...")

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
        if prob.prob_flag == 0:
            return render(request, 'challenge/list.html', dict(fail=True))
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
