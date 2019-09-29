# encoding: utf-8
from django.shortcuts import render,redirect,reverse

from rbac import models
# from rbac.forms.UserFrom import UserModelForm


def user_list(request):
    userList = models.UserInfos.objects.all()
    return render(request, 'rbac/user/user_list.html', locals())


def user_add(request):
    # if request.method == 'GET':
    #     form = UserModelForm()
    #
    # else:
    #     form = UserModelForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(reverse('user_list'))
    return render(request,'rbac/user/user_add.html',locals())


def user_edit(request):
    return None


def user_del(request):
    return None


def user_reset_pwd(request):
    return None
