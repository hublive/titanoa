from django.conf.urls import url

from web.views import base, work
from web.views import it
from web.views import prints
from web.views import basedata

urlpatterns = [
    # 基础设置
    url(r'login$', base.LoginView.as_view(), name='login'),
    url(r'lagout', base.lagout, name='lagout'),
    url(r'home', base.home, name='home'),
    url(r'reg', base.reg, name='reg'),

    # 基础数据
    url(r'organization/$', basedata.organization, name='organization'),
    url(r'userinfo/$', basedata.userinfo, name='userinfo'),
    url(r'computer/$', basedata.computer, name='computer'),
    url(r'property/$', basedata.property, name='property'),
    url(r'property/detail/(\d+)', basedata.property_detail, name='property_detail'),
    
    
    # 行政相关
    url(r'equipment/$', it.equipment, name='equipment'),
    url(r'baofei/$', it.baofei, name='baofei'),
    url(r'check/$', it.check, name='check'),
    url(r'fixedAssets/$', it.fixedAssets, name='fixedAssets'),
    url(r'fixedAssets_addr/$', it.fixedAssets_addr, name='fixedAssets_addr'),
    
    # 打印机
    url(r'prints/$', prints.prints, name='prints'),
    
    # 日常工作
    url(r'works/$', work.works, name='works'),
    url(r'wuliu/$', work.job_work, name='job_works'),
    url(r'wuliu_list/$', work.job_works, name='wuliu_list'),
    url(r'wuliu_detail/$', work.wuliu_detail, name='wuliu_detail'),
    url(r'job_detail/$', work.job_detail, name='job_detail'),
    
    # 到处excel
    url(r'cleck_excel/$', work.cleck_excel, name='cleck_excel'),
    url(r'job_excel/$', work.job_excel, name='job_excel'),
    url(r'print_excel/$', work.print_excel, name='print_excel'),
    url(r'equipment_excel/$', work.equipment_excel, name='equipment_excel'),
    url(r'fixedAssets_excel/$', work.fixedAssets_excel, name='fixedAssets_excel'),
    url(r'property_excel/$', work.property_excel, name='property_excel'),

]
