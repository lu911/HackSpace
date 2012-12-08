from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from admin.forms import ServerOnOffForm
from django.core.cache import *


@login_required(login_url='/login/')
def ServerOnOffView(request):
    form = ServerOnOffForm(request.POST)
    if form.is_valid():
        on_off_level = form.cleaned_data['on_off_level']
        cache.set('on_off_level', str(on_off_level))

    form = ServerOnOffForm()
    on_off_level = cache.get('on_off_level') 
    return render(request,'admin/server_on_off.html', dict(form=form, on_off_level = on_off_level))

