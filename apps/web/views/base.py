# encoding: utf-8
from django.contrib import auth
from django.shortcuts import render, redirect, reverse
from django.views import View

from web import models


# Create your views here.


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        user = auth.authenticate(username=username, password=pwd)
        if not user:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
        auth.login(request, user)
        return redirect(reverse('home'))


def lagout(request):
    auth.logout(request)
    return redirect(reverse('login'))


def home(request):
    return render(request, 'index.html')


def reg(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        models.User.objects.create_user(username=username, password=pwd)
        return redirect(reverse('login'))
    else:
        return render(request, 'reg.html')

