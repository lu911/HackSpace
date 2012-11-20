#-*-coding:utf-8-*-
from django.shortcuts import render
from django.http import HttpResponse

from member.models import UserProfile
from challenge.models import Problem, AuthLog

def ShowSolveStatusView(request):
    problems = Problem.objects.all()
    quantity = problems.count() + 1
    prob_id = []
    solved_prob_num = []

    for i in xrange(1,quantity):
        prob_id.append(i)
        solved_prob_num.append(0)

    print prob_id
    solved_prob = AuthLog.objects.filter(auth_type=1)
    for prob in solved_prob:
        print prob_id.index(prob.prob_id_id)
        position = prob_id.index(prob.prob_id_id)
        if position:
            solved_prob_num[position] += 1

    objects = []
    j = 0
    for i, prob in enumerate(solved_prob):
        objects = solved_prob[i]
        if objects is prob:
            if i == solved_prob_num[j]:
                j += 1
            
    return render(request, 'admin/show_solve_status.html', 
                            dict(problems=solved_prob,
                                 solved_prob_id=solved_prob_num))

def TestView(request):
    if request.method == 'POST':
        data1 = request.POST.get('data1')
        data2 = request.POST.get('data2')
        data = []
        data.append(data1)
        data.append(data2)
        return render(request, 'test.html', dict(data=data))
    else:
        pass
    return render(request, 'test.html')
