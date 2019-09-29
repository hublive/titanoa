# encoding: utf-8
import json
from io import BytesIO

import xlwt
from django.db.models import Q, Count, Sum
from django.http import HttpResponse
from django.shortcuts import render

from basedata.models import UserInfo, Property
from itcomputer.models import BaoFei, FixedAssets, Equipment, Check
from job import models
from job.models import JobDetail
from prints.models import Prints
from web.utils.get_values import get_values
from web.utils.kuaidi import kuadi
from web.utils.page import Pagination


def get_serarch_contion(request, query_list):
    query = request.GET.get('search', '')
    q = Q()
    q.connector = 'OR'
    for i in query_list:
        q.children.append(Q(('{}__contains'.format(i), query)))
    return q


def works(request):
    q = get_serarch_contion(request, ['createTime', 'username__name', 'typejobs__name'])
    all_num = models.JobDetail.objects.filter(q).count()
    all_job = models.JobDetail.objects.filter(q)
    jobs = models.JobDetail.objects.all()
    page = Pagination(request, all_job.count(), per_num=20)
    addr = models.JobDetail.objects.values('typejobs__name').all().distinct()
    dates = models.JobDetail.objects.values('createTime').distinct()
    dateList = []
    for item in dates:
        dateList.append(item['createTime'].strftime('%Y-%m'))
    addrList = get_values(addr)
    return render(request, 'work/work.html', {
        'all_job': all_job[page.start:page.end],
        'page': page,
        'jobs': jobs,
        'dateList': list(set(dateList)),
        'nameList': addrList,
        'all_num': str(all_num)
    })


def job_work(request):
    q = get_serarch_contion(request, ['name', ])
    all_work = models.JobWorks.objects.filter(q, status=False)
    all_jobwork = models.JobWorks.objects.all()
    page = Pagination(request, all_work.count(), per_num=20)
    return render(request, 'work/jobwork.html', {
        'all_work': all_work[page.start:page.end],
        'page': page,
        'all_jobwork': all_jobwork,
    })


def job_works(request):
    all_work = models.JobWorks.objects.all()
    return render(request, 'work/jobwork.html', {
        'all_work': all_work
    })


def wuliu_detail(request):
    nid = request.GET.get('nid')
    kudi_dict = kuadi(nid)
    kudi_dict = json.loads(kudi_dict)
    wuliu_dict = kudi_dict['result']
    request.session['wuliu_list'] = wuliu_dict['list']
    return render(request, 'work/wuliu_detail.html', )


def job_detail(request):
    # 分类展示
    # 1. 员工展示
    all_user_num = UserInfo.objects.all().count()
    user = UserInfo.objects.all().values('dept').order_by('dept').annotate(count=Count('dept'))
    # 2. 设备展示
    q = get_serarch_contion(request, ['p_time'])
    all_property = Property.objects.filter(q)
    all_property_num = all_property.count()
    p_name_count = all_property.values('p_name').order_by().annotate(count=Count('p_name'))
    p_brand_count = all_property.values('p_brand__name').order_by().annotate(count=Count('p_brand'))
    p_time_count = all_property.values('p_time').order_by().annotate(count=Count('p_time'))
    p_status_count = Property.objects.all().values('p_status').order_by().annotate(count=Count('p_status'))
    # 3. 工作展示
    q = get_serarch_contion(request, ['createTime'])
    all_jobdetail = JobDetail.objects.filter(q)
    all_jobdetail_num = all_jobdetail.count()
    j_type_count = all_jobdetail.values('typejobs__name').order_by().annotate(count=Count('typejobs__name'))
    j_time_count = all_jobdetail.values('createTime').order_by().annotate(count=Count('createTime'))
    # 4. 耗材展示
    q = get_serarch_contion(request, ['add_times'])
    all_print = Prints.objects.all().filter(q)
    all_print_num = all_print.count()
    model_name_count = all_print.values('model_name__name').order_by().annotate(count=Sum('num'))
    model_name_type_count = all_print.values('model_name_type__name').order_by().annotate(count=Sum('num'))
    p_addr = all_print.values('addr').order_by().annotate(count=Sum('num'))
    # 5. 固定资产展示
    q = get_serarch_contion(request, ['f_time'])
    all_fixed = FixedAssets.objects.filter(q)
    all_fixed_num = all_fixed.count()
    f_time_cout = all_fixed.values('f_time').order_by().annotate(count=Count('f_time'))
    f_addr_count = all_fixed.values('f_addr').order_by().annotate(count=Count('f_addr'))
    # 6. 设备升级展示
    q = get_serarch_contion(request, ['add_time'])
    all_equipment = Equipment.objects.filter(q)
    all_equipment_num = all_equipment.count()
    e_dept_count = all_equipment.values('propertys__p_user__name').order_by().annotate(
        count=Count('propertys__p_user__name'))
    e_model_count = all_equipment.values('model_name').order_by().annotate(count=Count('model_name'))
    e_model_price_count = all_equipment.values('model_name').order_by().annotate(sum=Sum('model_price'))
    e_time = all_equipment.values('add_time').order_by().annotate(count=Count('add_time'))
    # 7. 设备验收展示
    q = get_serarch_contion(request, ['c_time'])
    all_check = Check.objects.filter(q)
    all_check_num = all_check.count()
    c_time_count = all_check.values('c_time').order_by().annotate(count=Count('c_time'))
    c_gys_count = all_check.values('c_property__p_organization__name').order_by().annotate(
        count=Count('c_property__p_organization__name'))
    c_company_count = all_check.values('c_company').order_by().annotate(count=Count('c_company'))
    c_company_meary_count = all_check.values('c_company').order_by().annotate(sum=Sum('c_property__p_price'))
    # 8. 报废展示
    q = get_serarch_contion(request, ['b_time'])
    all_baofei_num = BaoFei.objects.filter(q).count()
    return render(request, 'work/job_detail.html', {
        # 1. 员工展示
        'all_user_num': all_user_num,
        'user': user,
        # 2. 设备展示
        'all_property_num': all_property_num,
        'p_name_count': p_name_count,
        'p_brand_count': p_brand_count,
        'p_time_count': p_time_count,
        'p_status_count': p_status_count,
        # 3. 工作展示
        'all_jobdetail_num': all_jobdetail_num,
        'j_type_count': j_type_count,
        'j_time_count': j_time_count,
        # 4. 耗材展示
        'all_print_num': all_print_num,
        'model_name_count': model_name_count,
        'model_name_type_count': model_name_type_count,
        'p_addr': p_addr,
        # 5. 固定资产展示
        'all_fixed_num': all_fixed_num,
        'f_time_cout': f_time_cout,
        'f_addr_count': f_addr_count,
        # 6. 设备升级展示
        'e_dept_count': e_dept_count,
        'e_model_count': e_model_count,
        'e_model_price_count': e_model_price_count,
        'all_equipment_num': all_equipment_num,
        'e_time': e_time,
        # 7. 设备验收展示
        'all_check_num': all_check_num,
        'c_time_count': c_time_count,
        'c_gys_count': c_gys_count,
        'c_company_count': c_company_count,
        'c_company_meary_count': c_company_meary_count,
        
        # 8. 报废展示
        'all_baofei_num': all_baofei_num,
        
    })


def cleck_excel(request):
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Titan_YS.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('设备验收')
    
    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)
    
    # 写入文件标题
    sheet.write(0, 0, '公司名称', style_heading)
    sheet.write(0, 1, '验收日期', style_heading)
    sheet.write(0, 2, '设备详情', style_heading)
    sheet.write(0, 3, '数量', style_heading)
    sheet.write(0, 4, '采购负责人', style_heading)
    sheet.write(0, 5, '订单编号', style_heading)
    sheet.write(0, 6, '外观检查', style_heading)
    sheet.write(0, 7, '验收结论', style_heading)
    sheet.write(0, 8, '验收人', style_heading)
    
    # 写入数据
    data_row = 1
    # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
    for i in Check.objects.all():
        print(i)
        # 格式化datetime
        sheet.write(data_row, 0, i.c_company)
        sheet.write(data_row, 1, i.c_time.strftime('%Y-%m-%d'))
        sheet.write(data_row, 2, i.c_property.p_id)
        sheet.write(data_row, 3, i.c_num)
        sheet.write(data_row, 4, i.c_caigou_name)
        sheet.write(data_row, 5, i.c_ghs_id)
        sheet.write(data_row, 6, i.c_ysbg_wg)
        sheet.write(data_row, 7, i.c_ysbg_jl)
        sheet.write(data_row, 8, i.c_ysr_name)
        data_row = data_row + 1
    
    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


def job_excel(request):
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Titan_work.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('工作明细')
    
    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)
    
    # 写入文件标题
    sheet.write(0, 0, '序号', style_heading)
    sheet.write(0, 1, '创建时间', style_heading)
    sheet.write(0, 2, '提交人', style_heading)
    sheet.write(0, 3, '问题类型', style_heading)
    sheet.write(0, 4, '问题描述', style_heading)
    sheet.write(0, 5, '完成状态', style_heading)
    sheet.write(0, 6, '维修人', style_heading)
    
    # 写入数据
    data_row = 1
    # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
    for i in JobDetail.objects.all():
        # 格式化datetime
        sheet.write(data_row, 0, i.id)
        sheet.write(data_row, 1, i.createTime.strftime('%Y-%m-%d'))
        sheet.write(data_row, 2, i.username.name)
        sheet.write(data_row, 3, i.typejobs.name)
        sheet.write(data_row, 4, i.note)
        sheet.write(data_row, 5, i.status)
        sheet.write(data_row, 6, i.jobuser)
        data_row = data_row + 1
    
    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


def print_excel(request):
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Titan_print.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('打印机耗材')
    
    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)
    
    # 写入文件标题
    sheet.write(0, 0, '序号', style_heading)
    sheet.write(0, 1, '申请人', style_heading)
    sheet.write(0, 2, '设备名称', style_heading)
    sheet.write(0, 3, '耗材名称', style_heading)
    sheet.write(0, 4, '申请时间', style_heading)
    sheet.write(0, 5, '数量', style_heading)
    sheet.write(0, 6, '所在地区', style_heading)
    sheet.write(0, 7, '备注', style_heading)
    
    # 写入数据
    data_row = 1
    # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
    for i in Prints.objects.all():
        # 格式化datetime
        sheet.write(data_row, 0, i.id)
        sheet.write(data_row, 1, i.add_times.strftime('%Y-%m-%d'))
        sheet.write(data_row, 2, i.userinfo.name)
        sheet.write(data_row, 3, i.model_name.name)
        sheet.write(data_row, 4, i.model_name_type.name)
        sheet.write(data_row, 5, i.num)
        sheet.write(data_row, 6, i.addr)
        sheet.write(data_row, 7, i.note)
        data_row = data_row + 1
    
    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


def equipment_excel(request):
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Titan_SJ.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('设备升级')
    
    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)
    
    # 写入文件标题
    sheet.write(0, 0, '序号', style_heading)
    sheet.write(0, 1, '申请时间', style_heading)
    sheet.write(0, 2, '维护类型', style_heading)
    sheet.write(0, 3, '设备编号', style_heading)
    sheet.write(0, 4, '设备配件', style_heading)
    sheet.write(0, 5, '单位', style_heading)
    sheet.write(0, 6, '数量', style_heading)
    sheet.write(0, 7, '维护金额', style_heading)
    sheet.write(0, 8, '维护负责人', style_heading)
    sheet.write(0, 9, '备注', style_heading)
    
    # 写入数据
    data_row = 1
    # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
    for i in Equipment.objects.all():
        # 格式化datetime
        sheet.write(data_row, 0, i.id)
        sheet.write(data_row, 1, i.add_time.strftime('%Y-%m-%d'))
        sheet.write(data_row, 2, i.type)
        sheet.write(data_row, 3, i.propertys.p_id)
        sheet.write(data_row, 4, i.model_name)
        sheet.write(data_row, 5, i.model_type.name)
        sheet.write(data_row, 6, i.model_num)
        sheet.write(data_row, 7, i.model_price)
        sheet.write(data_row, 8, i.model_username)
        sheet.write(data_row, 9, i.note)
        data_row = data_row + 1
    
    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


def fixedAssets_excel(request):
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Titan_GDZC.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('固定资产')
    
    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)
    
    # 写入文件标题
    sheet.write(0, 0, '序号', style_heading)
    sheet.write(0, 1, '员工姓名', style_heading)
    sheet.write(0, 2, '员工部门', style_heading)
    sheet.write(0, 3, '资产编号', style_heading)
    sheet.write(0, 4, '资产分类', style_heading)
    sheet.write(0, 5, '资产来源', style_heading)
    sheet.write(0, 6, '发放日期', style_heading)
    sheet.write(0, 7, '归属城市', style_heading)
    sheet.write(0, 8, '备注', style_heading)
    
    # 写入数据
    data_row = 1
    # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
    for i in Equipment.objects.all():
        # 格式化datetime
        sheet.write(data_row, 0, i.id)
        sheet.write(data_row, 1, i.f_property.p_user.name)
        sheet.write(data_row, 2, i.f_property.p_user.dept)
        sheet.write(data_row, 3, i.f_property.p_id)
        sheet.write(data_row, 4, i.f_property.p_brand.name)
        sheet.write(data_row, 5, i.f_property.p_organization.name)
        sheet.write(data_row, 6, i.f_time.strftime('%Y-%m-%d'))
        sheet.write(data_row, 7, i.f_addr)
        sheet.write(data_row, 9, i.f_note)
        data_row = data_row + 1
    
    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


def to_dict(self):
    return {
        'id': self.id,
        'p_id': self.p_id,
        'p_brand': self.p_brand.name,
        'p_sn': self.p_sn,
        'p_price': self.p_price,
        'p_status': self.p_status,
        'p_organization': self.p_organization.name,
        'f_note': self.p_user.name,
        'p_computers': self.p_computers.name,
        'p_endtime': self.p_endtime.strftime('%Y-%m-%d'),
    }


def property_excel(request):
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=Titan_ZC.xls'
    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('资产详情')
    
    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)
    
    # 写入文件标题
    sheet.write(0, 0, '序号', style_heading)
    sheet.write(0, 1, '资产ID', style_heading)
    sheet.write(0, 2, '资产名称', style_heading)
    sheet.write(0, 3, '资产品牌', style_heading)
    sheet.write(0, 4, '资产SN', style_heading)
    sheet.write(0, 5, '资产金额', style_heading)
    sheet.write(0, 6, '资产状态', style_heading)
    sheet.write(0, 7, '供应商', style_heading)
    sheet.write(0, 8, '资产详情', style_heading)
    sheet.write(0, 9, '领用时间', style_heading)
    
    # 写入数据
    data_row = 1
    # UserTable.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
    for i in Property.objects.all():
        # 格式化datetime
        sheet.write(data_row, 0, i.id)
        sheet.write(data_row, 1, i.p_id)
        sheet.write(data_row, 2, i.p_name)
        sheet.write(data_row, 3, i.p_brand.name)
        sheet.write(data_row, 4, i.p_sn)
        sheet.write(data_row, 5, i.p_price)
        sheet.write(data_row, 6, i.p_status)
        sheet.write(data_row, 7, i.p_organization.name)
        sheet.write(data_row, 8, i.p_computers.name)
        sheet.write(data_row, 9, i.p_time.strftime('%Y-%m-%d'))
        data_row = data_row + 1
    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response
