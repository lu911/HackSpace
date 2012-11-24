from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

def AdminUserManagerView(request):
    superusers = User.objects.filter(is_superuser=1)
    users = User.objects.filter(is_superuser=0)
    return render(request, 'admin/user_manager.html',
                            dict(superusers=superusers, users=users))

def AdminModifyUserView(request):
    prob_id = request.POST.get('user_id')
    if request.user.is_superuser:
        try:
            user = User.objects.get(id=user_id)
            default = {
                'username' : user.username,
                'password' : user.password,
                'is_staff' : user.is_staff,
                'is_superuser' : user.is_superuser,
            }
            if request.method == 'POST':
                form = UserForm(request.POST)
                if form.is_valid(): 
                    user.username = form.cleaned_data['username']
                    user.password = form.cleaned_data['password']
                    user.is_staff = form.cleaned_data['is_staff']
                    user.is_superuser = form.cleaned_data['is_superuser']
                    user.save()
            else:
                form = UserForm(initial=default)
        except User.DoesNotExist:
            pass
    else:
        pass
    return render(request,'',dict(form=form))

def AdminDeleteUserView(request):
    prob_id = request.GET.get('user_id')
    status = "FAIL"
    if request.user.is_superuser:
        try:
            prob = User.objects.get(id=user_id)
            prob.delete()
            status = "OK"
        except User.DoesNotExist:
            pass
    else:
        pass
    return HttpResponse(json.dumps(dict(status=status)), mimetype='application/json')
