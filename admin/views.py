#-*-coding:utf-8-*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from member.models import UserProfile
from challenge.models import Problem, AuthLog
from django.contrib.auth.models import User

def ShowSolveStatusView(request):
    problems = Problem.objects.all()
    quantity = problems.count() + 1
    prob_id = []
    solved_prob_num = []

    for i in xrange(1,quantity):
        prob_id.append(i)
        solved_prob_num.append(0)

    solved_prob = AuthLog.objects.filter(auth_type=1).order_by('prob_id')
    try:
        for prob in solved_prob:
            position = prob_id.index(prob.prob_id_id)
            solved_prob_num[position] += 1
    except ValueError:
        return render(request, 'admin/solve_status/render_solve_status.html',
                                dict(message='풀린 문제가 없습니다.'))

    sum = 0
    regulated_prob = []
    for num in solved_prob_num:
        sum += num
        regulated_prob.append(solved_prob[sum-1].prob_id.prob_name)

    return render(request, 'admin/solve_status/render_solve_status.html',
                            dict(problems=regulated_prob,
                                 solved_prob_num=solved_prob_num))

def ShowSolverStatusView(request, problem_name):
    problem = Problem.objects.get(prob_name=problem_name)
    solvers = AuthLog.objects.filter(prob_id=problem.id, auth_type=1)
    return render(request, 'admin/solve_status/solver_list.html',
                            dict(problem=problem_name,
                                 solvers=solvers))

def SearchSolverView(request):
    username = request.POST.get('username')
    try:
        user = User.objects.get(username=username)
        solver_info = AuthLog.objects.filter(user_id=user.id, auth_type=1).order_by('-auth_time')
        return render(request, 'admin/solve_status/user_solve_status.html',
                                dict(solver_info=solver_info,
                                     username=user.username))
    except:
        message = '존재하지 않는 ID입니다.'
        return render(request, 'admin/solve_status/user_solve_status.html',
                                dict(message=message))
