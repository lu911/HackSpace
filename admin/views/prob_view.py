#-*-coding:utf-8-*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from admin.forms import TagForm, ProblemForm
from challenge.models import Problem, TagName, ProbTag
import json

@login_required(login_url='/login/')
def AdminProblemListManagerView(request):
    if request.user.is_superuser:
        tags = TagName.objects.all()
        probs = {}
        for tag in tags:
            probs[tag.tag] = ProbTag.get_from_prob(tag.id)
        return render(request,'admin/challenge_manage/prob_list.html',dict(tags=tags,probs=probs))
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def AdminChallengeManagerView(request):
    if request.user.is_superuser:
        tags = TagName.objects.all()
        probs = {}
        for tag in tags:
            probs[tag.tag] = ProbTag.get_from_prob(tag.id)
        return render(request,'admin/challenge_manage/challenge_manager.html',dict(tags=tags,probs=probs))
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def AdminAddProblemManagerView(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ProblemForm(request.POST, request.FILES)
            if form.is_valid():
                problem = Problem(prob_name=form.cleaned_data['prob_name'],
                                  prob_content=form.cleaned_data['prob_content'],
                                  prob_point=form.cleaned_data['prob_point'],
                                  prob_auth=form.cleaned_data['prob_auth'],
                                  prob_flag=form.cleaned_data['prob_flag'],
                                  prob_file=form.cleaned_data['prob_file'])
                problem.save()
                tag = form.cleaned_data['prob_tag']
                if not tag:
                    tag = TagName.objects.get(id=1)
                ProbTag.objects.create(prob_id = problem, tag_id = tag)
        else:
            form = ProblemForm()
        return render(request,'admin/challenge_manage/prob_add_manager.html',dict(form=form))
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def AdminModifyProblemView(request):
    if request.user.is_superuser:
        prob_id = request.GET.get('prob_id')
        try:
            prob = Problem.objects.get(id=prob_id)
            prob_tag = ProbTag.objects.get(prob_id=prob_id)
            default = {
                'prob_name' : prob.prob_name,
                'prob_content' : prob.prob_content,
                'prob_point' : prob.prob_point,
                'prob_flag' : prob.prob_flag,
                'prob_tag'  : prob_tag.tag_id,
                'prob_file' : prob.prob_file
            }
            if request.method == 'POST':
                form = ProblemForm(request.POST, request.FILES)

                if form.is_valid():
                    prob.prob_name = form.cleaned_data['prob_name']
                    prob.prob_content = form.cleaned_data['prob_content']
                    if form.cleaned_data['prob_auth']:
                        prob.prob_auth = form.cleaned_data['prob_auth']
                    prob.prob_flag = form.cleaned_data['prob_flag']
                    prob.prob_point = form.cleaned_data['prob_point']
                    prob_tag.tag_id = form.cleaned_data['prob_tag']
                    if form.cleaned_data['prob_file']:
                        prob.prob_file = form.cleaned_data['prob_file']
                    prob.save()
                    prob_tag.save()
                    return HttpResponseRedirect(request.META['PATH_INFO'] + "?prob_id=" + prob_id)
            else:
                form = ProblemForm(initial=default)
            return render(request,'admin/challenge_manage/prob_modify_manager.html',dict(form=form))
        except Problem.DoesNotExist:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def AdminDeleteProblemView(request):
    if request.user.is_superuser:
        prob_id = request.GET.get('prob_id')
        status = "FAIL"
        try:
            prob = Problem.objects.get(id=prob_id)
            prob.delete()
            prob_tag = ProbTag.objects.filter(prob_id=prob_id).delete()
            status = "OK"
        except Problem.DoesNotExist:
            pass
    else:
        pass
    return HttpResponse(json.dumps(dict(status=status)), mimetype='application/json')

@login_required(login_url='/login/')
def AdminAddTagManagerView(request):
    if request.user.is_superuser:
        tags = TagName.objects.all()
        if request.method == 'POST':
            form = TagForm(request.POST)
            if form.is_valid():
                TagName.objects.create(tag=form.cleaned_data['tag'])
        else:
            form = TagForm(initial=request.GET)
        return render(request,'admin/challenge_manage/tag_add_manager.html',dict(form=form,tags=tags))
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def AdminModifyTagView(request):
    if request.user.is_superuser:
        tag_id = request.GET.get('tag_id')
        tag_name = request.POST.get('tag')
        try:
            tag = TagName.objects.get(id=tag_id)
            default = { 'tag' : tag.tag }
            if request.method == 'POST':
                form = TagForm(request.POST)
                if form.is_valid(): 
                    tag.tag = tag_name
                    tag.save()
            else:
                form = TagForm(initial=default)
        except:
            form = TagForm(initial=default)
        return render(request,'admin/challenge_manage/tag_modify_manager.html',dict(form=form)) 
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def AdminDeleteTagView(request):
    if request.user.is_superuser:
        tag_id = request.GET.get('tag_id')
        status = "FAIL"
        try:
            if tag_id == 1 or tag_id == "1":
                pass
            else:
                tag = TagName.objects.get(id=tag_id)
                prob_tag = ProbTag.objects.filter(tag_id=tag_id)
                etc_tag = TagName.objects.get(id=1)
                for tag in prob_tag:
                    tag.tag_id = etc_tag
                    tag.save()
                tag.delete()
                status = "OK"
        except TagName.DoesNotExist:
            pass
        return HttpResponse(json.dumps(dict(status=status)), mimetype='application/json')
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def AdminTagCheckView(request):
    if request.user.is_superuser:
        tag = request.GET.get('tag')
        status = "FAIL"
        try:
            tag_ = TagName.objects.get(tag=tag)
            status = "FAIL"
        except TagName.DoesNotExist:
            status = "OK"
        return HttpResponse(json.dumps(dict(status=status)), mimetype='application/json')
    else:
        return HttpResponseRedirect('/')
