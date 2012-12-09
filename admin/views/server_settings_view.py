from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from admin.forms import ServerOnOffForm, RankModeChangeForm
from django.core.cache import *


@login_required(login_url='/login/')
def ServerOnOffView(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    form = ServerOnOffForm(request.POST)
    if form.is_valid():
        on_off_level = form.cleaned_data['on_off_level']
        f=open("on_off", "wb")
        f.write(str(on_off_level))
        f.close()
        alert=True
    else:
        alert=False

    form = ServerOnOffForm()
    form2 = RankModeChangeForm()
    on_off_level = 0
    rank_mode = 0
    try:
        on_off_level = open("on_off", "r").read()
        rank_mode = open("rank_mode", "r").read()
    except:
        on_off_leve = "0"
        rank_mode = "0"
    return render(request,'admin/server_settings/server_settings.html', dict(form=form,
                                                                             form2=form2,
                                                                             rank_mode=rank_mode,
                                                                             on_off_level=on_off_level,
                                                                             on_off_level_alert=alert))

def CheckOnOffLevel(level):
    onOffLevel = "0"
    try:
        onOffLevel = open("on_off", "r").read()
    except:
        onOffLevel = "0"
    if int(onOffLevel) < level:
        return -1
    return int(onOffLevel)

def RankModeChangeView(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    form = RankModeChangeForm(request.POST)
    if form.is_valid():
        mode = form.cleaned_data['mode']
        f = open("rank_mode", "w")
        f.write(mode)
        f.close()
        alert=True
    else:
        alert=False

    form = ServerOnOffForm()
    form2 = RankModeChangeForm()
    on_off_level = 0
    rank_mode = 0
    try:
        on_off_level = open("on_off", "r").read()
        rank_mode = open("rank_mode", "r").read()
    except:
        on_off_leve = "0"
        rank_mode = "0"

    return render(request,'admin/server_settings/server_settings.html', dict(form=form,
                                                                             form2=form2,
                                                                             rank_mode=rank_mode,
                                                                             on_off_level=on_off_level,
                                                                             rank_mode_alert=alert))
