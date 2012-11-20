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
        form = AddProblemForm(request.POST)
        if form.is_valid():
            if request.user.is_superuser:
                problem = Problem(prob_name=form.cleaned_data['prob_name'],prob_content=form.cleaned_data['prob_content'],prob_point=form.cleaned_data['prob_point'],prob_auth=form.cleaned_data['prob_auth'],prob_flag=form.cleaned_data['prob_flag'])
                problem.save()
                ProbTag.objects.create(prob_id = problem, tag_id = form.cleaned_data['prob_tag'])
    else:
        form = AddProblemForm()
    return render(request,'admin/prob_manager.html',dict(form=form,tags=tags,probs=probs))

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


