from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import forms
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import json
import socket
from gui.models import cams


@login_required(login_url=reverse_lazy('login'))
def index(request):
    cam = cams.objects.all()
    return render(request,'index.html',{'cam':cam})

def loginuser(request):
    if len(get_user_model().objects.all()) == 0:
        return HttpResponseRedirect(reverse_lazy('install'))
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('index'))
    elif request.method == 'POST':
        form = forms.loginfrom(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['passwd']
            user = authenticate(request,username = username,password =password)
            print(user)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse_lazy('index'))
            else:
                return HttpResponseRedirect(reverse_lazy('login'))
    else:
        form = forms.loginfrom()
    return render(request,'login.html',{'form':form})    


def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))


def install(request):
    user = get_user_model()
    if len(get_user_model().objects.all()) == 0:
        if request.method == 'POST':
            if request.POST['password1'] ==request.POST['password2']:
                user.objects.create_superuser(username=request.POST['username'],password = request.POST['password1'],email = request.POST['email'])
                return HttpResponseRedirect(reverse_lazy('index'))
        return render(request,'install.html')
    else:
        return HttpResponseRedirect(reverse_lazy('login'))

def talkdaemon(msg):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('127.0.0.1',5998))
    s.send(msg.encode())
    data=s.recv(1024).decode
    s.close()
    return data

def camstab(request):
    cam = cams.objects.all()
    return render(request,'cams.html',{'cams':cam})