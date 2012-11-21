#-*-coding:utf-8-*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from member.models import UserProfile
from challenge.models import Problem, AuthLog, TagName, ProbTag
from admin.forms import TagForm, ProblemForm

import json


def ShowSolveStatusView(request):

    problems = Problem.objects.all()
    return render(request, 'admin/solve_status/render_solve_status.html',
                            dict(problems=problems))

def SearchUserView(request):
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
    prob_id = request.GET.get('prob_id')
    if request.user.is_superuser:
        try:
            prob = Problem.objects.get(id=prob_id)
            prob_tag = ProbTag.objects.get(prob_id=prob_id)
            default = {
                'prob_name' : prob.prob_name,
                'prob_content' : prob.prob_content,
                'prob_point' : prob.prob_point,
                'prob_auth' : prob.prob_auth,
                'prob_flag' : prob.prob_flag,
                'prob_tag'  : prob_tag.tag_id
            }
            if request.method == 'POST':
                form = ProblemForm(request.POST)
                if form.is_valid(): 
                    prob.prob_name = form.cleaned_data['prob_name']
                    prob.prob_content = form.cleaned_data['prob_content']
                    prob.prob_flag = form.cleaned_data['prob_flag']
                    prob.prob_auth = form.cleaned_data['prob_auth']
                    prob.prob_point = form.cleaned_data['prob_point']
                    prob_tag.tag_id = form.cleaned_data['prob_tag']
                    prob.save()
                    prob_tag.save()
                    return HttpResponseRedirect('/admin/prob/')
            else:
                form = ProblemForm(initial=default)
                
        except Problem.DoesNotExist:
            raise ValidationError("존재 하지 않는 문제입니다.")
    
    return render(request,'admin/prob_modify_manager.html',dict(form=form))

def AdminDeleteProblemView(request):
    prob_id = request.GET.get('prob_id')
    status = "FAIL"
    if request.user.is_superuser:
        try:
            prob = Problem.objects.get(id=prob_id)
            prob.delete()
            prob_tag = ProbTag.objects.filter(prob_id=prob_id).delete()
            status = "OK"
        except Problem.DoesNotExist:
            raise ValidationError("존재 하지 않는 문제입니다.")
    return HttpResponse(json.dumps(dict(status=status)), mimetype='application/json')

def AdminTagManagerView(request):
    tags = TagName.objects.all()
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            if request.user.is_superuser:
                TagName.objects.create(tag=form.cleaned_data['tag'])
    else:
        form = TagForm()
    return render(request,'admin/tag_manager.html',dict(form=form,tags=tags))

def AdminModifyTagView(request):
    tag_id = request.GET.get('tag_id')
    tag_name = request.POST.get('tag_name')
    if request.user.is_superuser:
        try:
            tag = TagName.objects.get(id=tag_id)
            default = {
                'tag' : tag.tag
            }
            if request.method == 'POST':
                form = TagForm(request.POST)
                if form.is_valid(): 
                    tag.tag = tag_name
                    tag.save()
                    return HttpResponseRedirect('/admin/tag/')
            else:
                form = TagForm(initial=default)
                
        except Tag.DoesNotExist:
            raise ValidationError("존재 하지 않는 태그입니다.")
    return render(request,'admin/tag_modify_manager.html',dict(form=form)) 

def AdminDeleteTagView(request):
    tag_id = request.GET.get('tag_id')
    status = "FAIL"
    if request.user.is_superuser:
        try:
            tag = TagName.objects.get(id=tag_id)
            prob_tag = ProbTag.objects.filter(tag_id=tag_id)
            for tag in prob_tag:
                tag.tag_id = 0
            prob_tag.save()
            tag.delete()
            status = "OK"
        except Tag.DoesNotExist:
            raise ValidationError("존재 하지 않는 태그입니다.")
    return HttpResponse(json.dumps(dict(status=status)), mimetype='application/json')

def AdminTagCheckView(request):
    tag = request.GET.get('tag')
    status = "FAIL"
    if request.user.is_superuser:
        try:
            tag_ = TagName.objects.get(tag=tag)
            status = "FAIL"
        except TagName.DoesNotExist:
            status = "OK"
    
    return HttpResponse(json.dumps(dict(status=status)), mimetype='application/json')


