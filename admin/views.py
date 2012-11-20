#-*-coding:utf-8-*-
from django.shortcuts import render

from django.http import HttpResponse

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
