#-*-coding:utf-8-*-
from member.models import *
from challenge.models import Problem, AuthLog
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

@login_required(login_url='/login/')
def ShowRankView(request):
    users = UserProfile.objects.order_by('-score')[:30]
    userlist = []
    for user in users:
        if user.score != 0:
            userlist.append(UserProfile(user))
    return render(request, 'rank/rank.html', dict(users=userlist))

def ShowRankGraphView(request):
    prob_num = Problem.objects.all()
    print prob_num.count()
    return HttpResponse('test')
