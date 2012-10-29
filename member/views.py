from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from member.forms import *

def MemberRegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST) #request.POST, request.FILES
        if form.is_valid():
            register_user(form)
            return HttpResponseRedirect('/login/')
    else:
        form = RegisterForm(initial=request.GET)
    return render(request, 'register.html', dict(form=form))

def register_user(form):
    user = User.objects.create_user(
        form.cleaned_data['username'],
        form.cleaned_data['password'],
        form.cleaned_data['email']
    )
    user.first_name = form.cleaned_data['nickname']
    user.save()
    UserProfile.objects.create(user=user,score=0)

def MemberLoginView(request):
    if request.method == 'POST':
        form = LoginForm()
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(request.POST.get('next', '/main/'))
    else:
        form = LoginForm()
    return render(request, 'login.html', dict(form=form, next=request.GET.get('next', '/login/')))

