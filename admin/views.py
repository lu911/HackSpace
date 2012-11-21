#-*-coding:utf-8-*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from member.models import UserProfile
from challenge.models import Problem, AuthLog, TagName, ProbTag
from admin.forms import AddTagForm, AddProblemForm

import json


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
    return render(request, 'admin/show_solve_status.html',
                            dict(problems=solved_prob,
                                 solved_prob_id=solved_prob_num))

def ShowSolverStatusView(request, problem_name):
    problem = Problem.objects.get(prob_name=problem_name)
    solvers = AuthLog.objects.filter(prob_id=problem.id, auth_type=1)
    return render(request, 'admin/solve_status/solver_list.html',
                            dict(problem=problem_name,
                                 solvers=solvers))

def AdminTagManagerView(request):
    tags = TagName.objects.all()
    if request.method == 'POST':
        form = AddTagForm(request.POST)
        if form.is_valid():
            if request.user.is_superuser:
                TagName.objects.create(tag=form.cleaned_data['tag'])
    else:
        form = AddTagForm()
    return render(request,'admin/tag_manager.html',dict(form=form,tags=tags))


def AdminProblemManagerView(request):
    tags = TagName.objects.all()
    probs = {}
    for tag in tags:
        probs[tag.tag] = ProbTag.get_from_prob(tag.id)
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            if request.user.is_superuser:
                problem = Problem(prob_name=form.cleaned_data['prob_name'],prob_content=form.cleaned_data['prob_content'],prob_point=form.cleaned_data['prob_point'],prob_auth=form.cleaned_data['prob_auth'],prob_flag=form.cleaned_data['prob_flag'])
                problem.save()
                ProbTag.objects.create(prob_id = problem, tag_id = form.cleaned_data['prob_tag'])
    else:
        form = ProblemForm()
    return render(request,'admin/prob_manager.html',dict(form=form,tags=tags,probs=probs))

def AdminModifyProblemView(request):
    prob_id = request.GEt.get('prob_id')
    if request.user.is_superuser:
        try:
            prob = Problem.objects.get(id=prob_id)
            prob_tag = ProbTag.objects.get(prob_id=prob_id)
            if request.method == 'POST':
                default = {
                    'prob_name' : prob.prob_name,
                    'prob_content' : prob.prob_content,
                    'prob_point' : prob.prob_point,
                    'prob_auth' : prob.prob_auth,
                    'prob_flag' : prob.prob_flag,
                    'prob_tag'  : prob_tag.tag
                }
            else:
                form = ProblemForm(initial=default)
            return render(request,'admin/prob_modify_manager.html',dict(form=form))
            
        
        
        except Problem.DoesNotExist:
            raise ValidationError("존재 하지 않는 문제입니다.")

def AdminTagCheckView(request):
    tag = request.POST.get('tag')
    status = "FAIL"
    if request.user.is_superuser:
        try:
            tag_ = TagName.object.get(tag=tag)
            status = "FAIL"
        except TagName.DoesNotExist:
            status = "OK"
    return render(request,json.dumps(dict(status=status)))


