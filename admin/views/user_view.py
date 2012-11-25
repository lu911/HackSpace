from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from member.models import UserProfile
from admin.forms import UserForm

import json


def AdminUserInfoView(request):
    user_id=request.GET.get('user_id')
    user = User.objects.get(id=user_id)
    data=dict(
        user_id=user.id,
        username=user.username, 
        is_staff=user.is_staff,
        is_superuser=user.is_superuser
    )
    return HttpResponse(json.dumps(data), mimetype='application/json')

def AdminUserManagerView(request):
    form = UserForm()
    all_users=dict()
    super_users = User.objects.filter(is_superuser=1).order_by("last_login")
    normal_users = User.objects.filter(is_superuser=0).order_by("last_login")
    all_users['super-users']={
        "users":super_users[:10],
        "page_count":range(1, int(super_users.count()/10)+2)
    }
    all_users['normal-users']={
        "users":normal_users[:10],
        "page_count":range(1, int(normal_users.count()/10)+2)
    }
    return render(request,'admin/user_manager.html', dict(all_users=all_users, form=form))

   

def AdminUserListManagerView(request):
    user_page=int(request.GET.get('user_page'))-1
    superuser_page=int(request.GET.get('superuser_page'))-1
    form = UserForm()
    all_users=dict()
    super_users = User.objects.filter(is_superuser=1).order_by("last_login")
    normal_users = User.objects.filter(is_superuser=0).order_by("last_login")
    all_users['super-users']={
        "users":super_users[10*superuser_page:10*superuser_page+10],
        "page_count":range(1, int(super_users.count()/10)+2)
    }
    all_users['normal-users']={
        "users":normal_users[10*user_page:10*user_page+10],
        "page_count":range(1, int(normal_users.count()/10)+2)
    }
    return render(request, 'admin/user_list.html',
                            dict(all_users=all_users, user_page=user_page+1, superuser_page=superuser_page+1))

def AdminModifyUserView(request):
    user_id = request.POST.get('user_id')
    result="ERROR"
    if request.user.is_superuser:
        try:
            user = User.objects.get(id=user_id)
            form = UserForm(request.POST)
            print form.errors
            if form.is_valid():
                print form.cleaned_data['is_superuser']
                print type(form.cleaned_data['is_superuser'])
                user.username = form.cleaned_data['username']
                user.set_password(form.cleaned_data['password'] or user.password)
                user.is_staff = form.cleaned_data['is_staff']
                user.is_superuser = form.cleaned_data['is_superuser']
                user.save()
                result="Done"
        except User.DoesNotExist:
            pass
    else:
        result="You are not superuser"
    return HttpResponse(result)     

def AdminDeleteUserView(request):
    user_id = request.GET.get('user_id')
    status = "FAIL"
    if request.user.is_superuser:
        try:
            user = User.objects.get(id=user_id)
            profile = UserProfile.objects.get(user=user)
            user.delete()
            profile.delete()
            status = "OK"
        except User.DoesNotExist:
            pass
    else:
        pass
    return HttpResponse(json.dumps(dict(status=status)), mimetype='application/json')
