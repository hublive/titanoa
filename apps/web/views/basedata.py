# encoding: utf-8
from django.db.models import Q
from django.shortcuts import render

from basedata import models
from job import models as job_model
from web.utils.get_values import get_values
from web.utils.page import Pagination


def get_serarch_contion(request, query_list):
    query = request.GET.get('search', '')
    q = Q()
    q.connector = 'OR'
    for i in query_list:
        q.children.append(Q(('{}__contains'.format(i), query)))
    return q


def organization(request):
    q = get_serarch_contion(request, ['name', 'users__name'])
    all_organization = models.Organization.objects.filter(q)
    pag = Pagination(request, all_organization.count(), per_num=10)
    username = models.Organization.objects.all().values('users__name').distinct()
    return render(request, 'base/organization.html', {
        'all_organization': all_organization[pag.start:pag.end],
        'pag': pag,
        'username': username,
    })


def userinfo(request):
    q = get_serarch_contion(request, ['name', 'dept'])
    all_user = models.UserInfo.objects.filter(q)
    page = Pagination(request, all_user.count(), per_num=10)
    dept_list = []
    dept_obj = models.UserInfo.objects.all().values('dept').distinct()
    
    # 处理部门字段
    for item in dept_obj:
        for key, value in item.items():
            dept = '-'.join(value.split('-')[1:2])
            dept_list.append(dept)
    
    deptList = list(set(dept_list))
    
    return render(request, 'base/userinfo.html', {
        'all_user': all_user[page.start:page.end],
        'page': page,
        'dept_list': deptList,
    })


def computer(request):
    q = get_serarch_contion(request, ['name','memory'])
    all_computer = models.Computer.objects.filter(q)
    pag = Pagination(request, all_computer.count(), per_num=8)
    return render(request, 'base/computer.html', {
        'all_computer': all_computer[pag.start:pag.end],
        'page': pag,
    })


def property(request):
    q = get_serarch_contion(request, ['p_id', 'p_user__name','p_status'])
    all_property = models.Property.objects.filter(q)
    all_num = models.Property.objects.filter(q).count()
    pag = Pagination(request, all_property.count(), per_num=15)
    status = models.Property.objects.all().values('p_status')
    statusList = get_values(status)
    return render(request, 'base/property.html', {
        'all_property': all_property[pag.start:pag.end],
        'page': pag,
        'all_num': all_num,
        'statusList': statusList,
    })


def property_detail(request,pid):
    property_obj = models.Property.objects.filter(p_id=pid)
    job_obj = job_model.JobDetail.objects.filter(username__property__p_id=pid)
    property_price = models.Property.objects.filter(p_id=pid).values('equipment__model_price')
    return render(request,'base/property_detail.html',locals())
