#-*-coding:utf-8-*-
from member.models import *
from challenge.models import Problem, AuthLog

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

@login_required(login_url='/login/')
def ShowRankView(request):
    users = UserProfile.objects.order_by('-score')[:30]
    userlist = []
    for user in users:
        if user.score != 0:
            userlist.append(UserProfile(user))
    return render(request, 'rank/rank.html', dict(users=userlist))

def ShowRankGraphView(request):
    users = UserProfile.objects.filter(~Q(score=0)).order_by('id')
    solvers = AuthLog.objects.filter(auth_type=1).order_by('id')

    solver_list = [ solver.user_id.username for solver in solvers ]
    scores = [[0]*0 for i in xrange(users.count())]
    user = [ user.user.username for user in users ]


    sum = 0
    j = 0
    for i, solver in enumerate(solvers):
        if user[j] == solver_list[i]:
            sum += int(solver.prob_id.prob_point)
            scores[j].append(sum)
        else:
            j += 1
            scores[j].append(int(solver.prob_id.prob_point))

    data = []
    for i, score in enumerate(scores):
        data.append(dict(name=user[i],scores=score))
    
    return render(request, 'rank/rank2.html', dict(users=users,
                                                   data=data))
