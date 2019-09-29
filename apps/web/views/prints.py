# encoding: utf-8
from django.db.models import Q
from django.shortcuts import render

from prints import models
from web.utils.get_values import get_values
from web.utils.page import Pagination


def get_serarch_contion(request, query_list):
    query = request.GET.get('search', '')
    q = Q()
    q.connector = 'OR'
    for i in query_list:
        q.children.append(Q(('{}__contains'.format(i), query)))
    return q


def prints(request):
    q = get_serarch_contion(request, ['userinfo__name', 'add_times', 'addr'])
    all_prints = models.Prints.objects.filter(q)
    all_num = models.Prints.objects.filter(q).count()
    prints = models.Prints.objects.all()
    page = Pagination(request, all_prints.count(), per_num=15)
    addr = models.Prints.objects.values('addr').all().distinct()
    dates = models.Prints.objects.values('add_times').distinct()
    dateList = []
    for item in dates:
        dateList.append(item['add_times'].strftime('%Y-%m'))
    addrList = get_values(addr)
    return render(request, 'print/print.html', {
        'all_prints': all_prints[page.start:page.end],
        'page': page,
        'prints': prints,
        'all_num':all_num,
        'dateList': list(set(dateList)),
        'nameList': addrList,
    })
