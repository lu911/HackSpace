from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

def AdminUserManagerView(request):
    users = User.objects.all()
    return render(request, 'admin/user_manager.html',
                            dict(users=users))
