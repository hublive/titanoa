from datetime import datetime

from django.db import models
# Create your models here.
from django.utils.html import format_html


class UserInfo(models.Model):
    name = models.CharField(max_length=24, verbose_name='员工姓名', unique=True)
    dept = models.CharField(max_length=32, verbose_name='部门名称')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "员工信息"
        verbose_name_plural = verbose_name


class Warehouse(models.Model):
    code = models.CharField(max_length=6, verbose_name='仓库编号', blank=True, null=True)
    name = models.CharField(max_length=40, verbose_name='仓库名称', unique=True)
    location = models.CharField(max_length=120, verbose_name='位置')
    users = models.ManyToManyField(to='UserInfo', verbose_name='仓库管理员', blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "仓库信息"
        verbose_name_plural = verbose_name


class Measure(models.Model):
    name = models.CharField(max_length=20, verbose_name='单位名称', unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "单位类型"
        verbose_name_plural = verbose_name


class Brand(models.Model):
    name = models.CharField(max_length=120, verbose_name='品牌名称', unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "品牌信息"
        verbose_name_plural = verbose_name


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='分类名称', unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "分类信息"
        verbose_name_plural = verbose_name


class Material(models.Model):
    code = models.CharField(max_length=20, verbose_name='物品编号', blank=True, null=True, unique=True)
    name = models.CharField(max_length=120, verbose_name='商品名称', unique=True)
    materialImg = models.ImageField(upload_to='Material/%Y%m', default='Material/default.png', max_length=100,
                                    verbose_name='物品图片', null=True)
    spec = models.CharField(max_length=120, verbose_name='规格/型号', blank=True, null=True)
    brand = models.ForeignKey(to="Brand", blank=True, null=True, verbose_name='品牌', on_delete=models.CASCADE)
    category = models.ForeignKey(to="Category", verbose_name='物品分类', blank=True, null=True, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(to='Warehouse', blank=True, null=True, verbose_name="所属仓库", on_delete=models.CASCADE)
    measures = models.ForeignKey(to="Measure", blank=True, verbose_name="物品单位", on_delete=models.CASCADE)
    stock_price = models.DecimalField(verbose_name="单价", max_digits=14, decimal_places=2, blank=True, null=True)
    
    def image_data(self):
        return format_html(
            '<img src="/media/{}" style="width: 80px;height: 60px"/>'.format(self.materialImg)
        )
    
    image_data.short_description = u'物品图片'
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']
        verbose_name = "物品信息"
        verbose_name_plural = verbose_name


class Organization(models.Model):
    name = models.CharField(verbose_name="供应商名称", max_length=20, unique=True)
    users = models.ForeignKey(to="UserInfo", on_delete=models.CASCADE, null=True, blank=True, verbose_name="所属人")
    type = models.CharField(max_length=20, verbose_name='供应商类型', choices=(('gt', '个体经营'), ('hlw', '互联网')))
    phone = models.CharField(max_length=13, verbose_name='联系电话', null=True, blank=True, default='88888888')
    addr = models.CharField(max_length=24, verbose_name='地址', null=True, default='上海')
    status = models.BooleanField(verbose_name="是否启用", default=True)
    note = models.TextField(verbose_name='说明', default=None, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "供应商"
        verbose_name_plural = verbose_name


class Computer(models.Model):
    name = models.CharField(max_length=32, verbose_name='设备名称', help_text='设备名称')
    type = models.CharField(max_length=32, verbose_name='设备类型', choices=(
        ('品牌台式电脑', '品牌台式电脑'),
        ('笔记本电脑', '笔记本电脑'),
        ('组装台式机', '组装台式机'),
        ('打印机', '打印机'),
        ('投影仪', '投影仪'),
    ), help_text='设备类型')
    mainboard = models.CharField(max_length=64, verbose_name='主板', default='Intel', null=True, blank=True)
    CPU = models.CharField(max_length=64, verbose_name='CPU', null=True, blank=True)
    memory = models.CharField(max_length=64, verbose_name='内存', null=True, blank=True)
    disk = models.CharField(max_length=64, verbose_name='硬盘', null=True, blank=True)
    video = models.CharField(max_length=64, verbose_name='显卡', choices=(('集成显卡', '集成显卡'), ('独立显卡', '独立显卡'), ('无', '无')),
                             default='集成显卡', null=True, blank=True)
    displayer = models.CharField(max_length=64, verbose_name='显示器', default='14英寸', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "配置详情"
        verbose_name_plural = verbose_name


class Property(models.Model):
    p_id = models.CharField(max_length=32, verbose_name='资产ID', unique=True, null=False)
    p_name = models.CharField(max_length=32, verbose_name='资产名称')
    p_brand = models.ForeignKey(to="Brand", null=True, blank=True, on_delete=models.CASCADE,
                                verbose_name="资产品牌")
    p_sn = models.CharField(max_length=32, verbose_name='资产SN(序列号)', unique=True, null=False)
    p_price = models.IntegerField(verbose_name='资产金额')
    p_image = models.ImageField(upload_to='property/%Y-%m-%d', default='image/default.png', max_length=100,
                                verbose_name='资产图片', null=True, blank=True)
    p_status = models.CharField(max_length=32, verbose_name='资产状态', default='未用', choices=(
        ('在用', '在用'),
        ('未用', '未用'),
        ('报废', '报废'),
    ))
    p_organization = models.ForeignKey(to="Organization", null=True, blank=True, on_delete=models.CASCADE,
                                       verbose_name="供应商")
    p_user = models.ForeignKey(to="UserInfo", on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name="员工")
    p_computers = models.ForeignKey(to="Computer", verbose_name='资产详情', on_delete=models.CASCADE, null=True, blank=True)
    p_time = models.DateField(verbose_name='创建时间', auto_created=datetime.now)
    p_endtime = models.DateTimeField(verbose_name='领取时间', auto_now=datetime.now, null=True, blank=True)
    
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
    
    def image_data(self):
        return format_html(
            '<img src="/media/{}" style="width: 80px;height: 60px"/>',
            self.p_image,
        )
    
    image_data.short_description = '机器图片'
    
    def model_price(self):
        sum = 0
        for item in self.equipment_set.all():
            sum += item.model_price
        return sum
    
    def sum_price(self):
        price = self.model_price()
        return self.p_price + price
    
    def __str__(self):
        return self.p_id
    
    class Meta:
        ordering = ['-p_id']
        verbose_name = "资产详情"
        verbose_name_plural = verbose_name
