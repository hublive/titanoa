# encoding: utf-8
from django.db.models import Q
from django.shortcuts import render

from itcomputer import models
from web.utils.get_values import get_values
from web.utils.page import Pagination


def get_serarch_contion(request, query_list):
    query = request.GET.get('search', '')
    q = Q()
    q.connector = 'OR'
    for i in query_list:
        q.children.append(Q(('{}__contains'.format(i), query)))
    return q


def equipment(request):
    q = get_serarch_contion(request, ['propertys__p_id', 'add_time', 'type', 'model_username'])
    all_equipment = models.Equipment.objects.filter(q)
    page = Pagination(request, all_equipment.count(), per_num=15)
    types = models.Equipment.objects.values('type').all().distinct()
    model_username = models.Equipment.objects.values('model_username').all().distinct()
    typeList = get_values(types)
    nameList = get_values(model_username)
    return render(request, 'it/equipment.html', {
        'all_equipment': all_equipment[page.start:page.end],
        'page': page,
        'typeList': typeList,
        'nameList': nameList,
    })


def baofei(request):
    q = get_serarch_contion(request, ['b_time', 'b_userinfo__name', 'b_ids__p_id', 'b_way'])
    all_baofei = models.BaoFei.objects.filter(q)
    all_baofeis = models.BaoFei.objects.all()
    page = Pagination(request, all_baofei.count(), per_num=20)
    whys = models.BaoFei.objects.values('b_way').all().distinct()
    dates = models.BaoFei.objects.values('b_time').distinct()
    dateList = []
    for item in dates:
        dateList.append(item['b_time'].strftime('%Y-%m'))
    whyList = get_values(whys)
    return render(request, 'it/baofei.html', {
        'all_baofei': all_baofei[page.start:page.end],
        'all_baofeis': all_baofeis,
        'page': page,
        'dateList': dateList,
        'whyList': whyList,
    })


def check(request):
    q = get_serarch_contion(request, ['c_company', 'c_time', 'c_caigou_name'])
    all_check = models.Check.objects.filter(q)
    all_checks = models.Check.objects.all()
    page = Pagination(request, all_check.count(), per_num=20)
    name = models.Check.objects.values('c_company').all().distinct()
    dates = models.Check.objects.values('c_time').distinct()
    dateList = []
    for item in dates:
        dateList.append(item['c_time'].strftime('%Y-%m'))
    nameList = get_values(name)
    return render(request, 'it/check.html', {
        'all_check': all_check[page.start:page.end],
        'all_checks': all_checks,
        'page': page,
        'name': name,
        'dateList': dateList,
        'nameList': nameList,
    })


def fixedAssets(request):
    q = get_serarch_contion(request, ['f_time', 'f_property__p_id', 'f_property__p_user__name'])
    all_fixedAssets = models.FixedAssets.objects.filter(q)
    all_fixeds = models.FixedAssets.objects.all()
    page = Pagination(request, all_fixedAssets.count(), per_num=20)
    dates = models.FixedAssets.objects.values('f_time').distinct()
    dateList = []
    for item in dates:
        dateList.append(item['f_time'].strftime('%Y-%m'))
    return render(request, 'it/fixeassets.html', {
        'all_fixedAssets': all_fixedAssets,
        'all_fixeds': all_fixeds[page.start:page.end],
        'page': page,
        'dateList': list(set(dateList)),
    })


def fixedAssets_addr(request):
    f_id = request.GET.get('f_id')
    all_fixed = models.FixedAssets.objects.filter(f_property__p_id=f_id)
    return render(request, 'it/addr.html', {
        'all_fixed': all_fixed
    })
