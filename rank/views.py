#-*-coding:utf-8-*-
from member.models import *
from challenge.models import *
from django.contrib.auth.models import User
from django.shortcuts import render

def ShowRankView(request):
    users = UserProfile.objects.order_by('-score')[:10]
    userlist = []
    for user in users:
        if user.score != 0:
            userlist.append(UserProfile(user))
    return render(request, 'rank/rank.html', dict(users=userlist))
