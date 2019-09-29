from django.db import models
# Create your models here.
from django.utils import timezone

from basedata.models import Property
from basedata.models import UserInfo

c_company_type = (
    ('上海泰坦科技股份有限公司', '上海泰坦科技股份有限公司'),
    ('上海蒂剀姆溶剂有限公司', '上海蒂剀姆溶剂有限公司'),
)


class Check(models.Model):
    c_company = models.CharField(max_length=32, verbose_name='公司名称', choices=c_company_type, default='上海泰坦科技股份有限公司')
    c_time = models.DateField(verbose_name='验收日期', auto_now=timezone.now)
    c_property = models.ForeignKey(to="basedata.Property", default=None, blank=True, null=True,
                                   verbose_name='设备详情', to_field='p_id', on_delete=models.CASCADE)
    c_num = models.IntegerField(verbose_name='数量', default=1)
    c_caigou_name = models.CharField(max_length=32, verbose_name='采购负责人', default='王佳', choices=(
        ('王佳', '王佳'),
        ('胡兵', '胡兵'),
    ))
    c_ghs_id = models.CharField(max_length=32, verbose_name='订单编号')
    c_ysbg_wg = models.BooleanField(verbose_name='外观检查', default=True)
    c_ysbg_jl = models.BooleanField(verbose_name='验收结论', default=True)
    c_ysr_name = models.CharField(max_length=32, verbose_name='验收人', default='胡兵')
    
    def to_dict(self):
        return {
            'c_company': self.c_company,
            'c_time': self.c_time.strftime('%Y-%m-%d'),
            'c_property': self.c_property.p_id,
            'c_num': self.c_num,
            'c_caigou_name': self.c_caigou_name,
            'c_ghs_id': self.c_ghs_id,
            'c_ysbg_wg': self.c_ysbg_wg,
            'c_ysbg_jl': self.c_ysbg_jl,
            'c_ysr_name': self.c_ysr_name
        }
    
    def __str__(self):
        return '(%s)' % (self.c_caigou_name)
    
    class Meta:
        verbose_name = "设备验收"
        verbose_name_plural = verbose_name


class BaoFei(models.Model):
    """申请人，部门，设备名称，核定人"""
    b_time = models.DateField(verbose_name='登记日期', default=timezone.now)
    b_userinfo = models.ForeignKey(to="basedata.UserInfo", verbose_name='申请人',
                                   on_delete=models.CASCADE)
    b_ids = models.ForeignKey(to="basedata.Property", default=None, blank=True, null=True,
                              verbose_name='设备详情', to_field='p_id', on_delete=models.CASCADE)
    b_way = models.CharField(verbose_name='报废原因', choices=(
        ('自然损坏', '自然损坏'),
        ('非自然损坏', '非自然损坏'),
        ('满足不了业务需求', '满足不了业务需求'),
        ('超过使用年限', '超过使用年限'),
        ('其他原因', '其他原因'),
    ), default=None, max_length=10)
    b_num = models.IntegerField(verbose_name='数量', default=1)
    b_note = models.CharField(max_length=200, verbose_name='备注', default='空')
    
    def to_dict(self):
        return {
            'id': self.id,
            'b_time': self.b_time.strftime('%Y-%m-%d'),
            'b_userinfo': self.b_userinfo.name,
            'b_ids': self.b_ids.p_id,
            'b_way': self.b_way,
            'b_num': self.b_num,
            'b_note': self.b_note,
        }
    
    def __str__(self):
        return self.b_ids.p_id
    
    class Meta:
        verbose_name = "设备报废"
        verbose_name_plural = verbose_name


class FixedAssets(models.Model):
    f_time = models.DateField(verbose_name='发放日期', auto_created=timezone.now)
    f_property = models.ForeignKey(to="basedata.Property", verbose_name='设备详情',to_field='p_id', on_delete=models.CASCADE)
    f_addr = models.CharField(max_length=32, verbose_name='归属城市')
    f_note = models.CharField(max_length=200, verbose_name='备注')
    
    def __str__(self):
        return self.f_addr
    
    class Meta:
        ordering = ['id']
        verbose_name = "固定资产"
        verbose_name_plural = verbose_name
        
    def to_dict(self):
        return {
            'id': self.id,
            'f_property_username': self.f_property.p_user.name,
            'f_property_userdept': self.f_property.p_user.dept,
            'f_property': self.f_property.p_id,
            'f_property_brand': self.f_property.p_brand.name,
            'f_property_or': self.f_property.p_organization.name,
            'f_time': self.f_time.strftime('%Y-%m-%d'),
            'f_addr': self.f_addr,
            'f_note': self.f_note,
        }


class Equipment(models.Model):
    add_time = models.DateField(verbose_name='申请时间', default=timezone.now)
    type = models.CharField(max_length=32, verbose_name='类型', choices=(
        ('升级设备', '升级设备'),
        ('维修设备', '维修设备'),
    ), default='升级设备')
    propertys = models.ForeignKey(to="basedata.Property", verbose_name='设备编号', to_field='p_id',
                                  on_delete=models.CASCADE)
    model_name = models.CharField(max_length=12, verbose_name='设备配件')
    model_type = models.ForeignKey(to="basedata.Measure", on_delete=models.CASCADE, verbose_name='单位', default=1)
    model_num = models.IntegerField(verbose_name='数量', default=1)
    model_price = models.IntegerField(verbose_name='金额', default=0)
    model_username = models.CharField(max_length=32, verbose_name='维修负责人', choices=(
        ('胡兵', '胡兵'),
        ('杨学铭', '杨学铭'),
    ), default='胡兵')
    note = models.CharField(max_length=200, verbose_name='备注', default='无')
    def to_dict(self):
        return {
            'id': self.id,
            'add_time': self.add_time.strftime('%Y-%m-%d'),
            'type': self.type,
            'propertys': self.propertys.p_id,
            'model_name': self.model_name,
            'model_type': self.model_type.name,
            'model_num': self.model_num,
            'model_price': self.model_price,
            'model_username': self.model_username,
            'note': self.note,
        }
    def sum(self):
        return int(Property.p_price + self.model_price)
    
    def __str__(self):
        return self.model_name
    
    class Meta:
        ordering = ['-id']
        verbose_name = "设备升级"
        verbose_name_plural = verbose_name
