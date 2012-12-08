#-*-coding:utf-8-*-
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from challenge.models import Problem, AuthLog

@login_required(login_url='/login/')
def ShowSolveStatusView(request):
    if request.user.is_superuser:
        all_problems = Problem.objects.all()
        solved_problems = Problem.objects.filter(~Q(prob_solver=0)).order_by('-prob_solver')[:10]
        return render(request, 'admin/solve_status/render_solve_status.html',
                                dict(all_problems=all_problems,
                                     solved_problems=solved_problems))
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def SearchUserView(request):
    if request.user.is_superuser:
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            solver_info = AuthLog.objects.filter(user_id=user.id, auth_type=1).order_by('auth_time')
            sum = 0
            scores = []
            for info in solver_info:
                sum += info.prob_id.prob_point
                scores.append(sum)
            if sum == 0:
                score = False
            else:
                score = True
            return render(request, 'admin/solve_status/user_solve_status.html',
                                    dict(solver_info=solver_info,
                                         scores=scores,
                                         username=user.username,
                                         chart_render=True,
                                         score=score))
        except:
            message = 'not exist user.'
            return render(request, 'admin/solve_status/user_solve_status.html',
                                    dict(message=message,
                                         chart_render=False))
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def ShowSolverStatusView(request, prob_id):
    if request.user.is_superuser:
        problem = Problem.objects.get(id=prob_id)
        solvers = AuthLog.objects.filter(prob_id=problem.id, auth_type=1)
        return render(request, 'admin/solve_status/solver_list.html',
                                dict(problem=problem,
                                     solvers=solvers))
    else:
        return HttpResponseRedirect('/')
