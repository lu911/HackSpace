#-*-coding:utf-8-*-
from member.forms import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth import login, logout

def memberRegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            register_user(form)
            return HttpResponseRedirect('/login/')
    else:
        form = RegisterForm(initial=request.GET)
    return render(request, 'registration/register.html', dict(form=form))

def register_user(form):
    user = User.objects.create_user(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password'],
        email=form.cleaned_data['email']
    )
    user.first_name = form.cleaned_data['nickname']
    user.save()
    UserProfile.objects.create(user=user,score=0)

def memberLoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            print user
            login(request, user)
            return HttpResponseRedirect(request.POST.get('next', '/login/'))
        else:
            return HttpResponseRedirect(request.GET.get('next', '/login/'))
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', dict(form=form, next=request.GET.get('next', '/login/')))

def memberLogout(request):
    logout(request)
    return HttpResponseRedirect('/login/')
