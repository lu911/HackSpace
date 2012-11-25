from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from member.models import UserProfile
from admin.forms import UserForm
from collections import OrderedDict

import json

def AdminUserInfoView(request):
    user_id=request.GET.get('user_id')
    user = User.objects.get(id=user_id)
    data=dict(
        user_id=user.id,
        username=user.username, 
        is_staff=user.is_staff,
        is_superuser=user.is_superuser,
        is_active=user.is_active
    )
    return HttpResponse(json.dumps(data), mimetype='application/json')

def AdminUserManagerView(request):
    groups={"super", "active", "block"};
    form = UserForm()
    pages_count=dict()
    all_users={
        "super-users" : 
            User.objects.filter(is_superuser=1).order_by("last_login"),
        "active-users" : 
            User.objects.filter(is_superuser=0, is_active=1).order_by("last_login"),
        "block-users" : 
            User.objects.filter(is_superuser=0, is_active=0).order_by("last_login")
    }
    for k, v in  all_users.iteritems():
        all_users[k]=v[:10]
        pages_count[k]=int(v.count()/10)+1
    all_users=OrderedDict(sorted(all_users.items()))
    return render(request,'admin/user_manager.html', dict(groups=groups, all_users=all_users, pages_count=pages_count, form=form))

   

def AdminUserListManagerView(request):
    groups={"super", "active", "block"};
    pages={
        "active-users" :int(request.GET.get('active_user_page')),
        "block-users" :int(request.GET.get('block_user_page')),
        "super-users" : int(request.GET.get('super_user_page'))
    }
    pages_count=dict()
    all_users={
        "super-users" : 
            User.objects.filter(is_superuser=1).order_by("last_login"),
        "active-users" : 
            User.objects.filter(is_superuser=0, is_active=1).order_by("last_login"),
        "block-users" : 
            User.objects.filter(is_superuser=0, is_active=0).order_by("last_login")
    }
    for k, v in  all_users.iteritems():
        all_users[k]=v[10*(pages[k]-1):10*(pages[k]-1)+10]
        pages_count[k]=int(v.count()/10)+1
        
    all_users=OrderedDict(sorted(all_users.items()))
    return render(request, 'admin/user_list.html',
                            dict(groups=groups, all_users=all_users, pages=pages, pages_count=pages_count))

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
                user.is_active = form.cleaned_data['is_active']
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
