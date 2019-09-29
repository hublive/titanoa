from django.db import models
# Create your models here.
from django.utils import timezone

from basedata.models import UserInfo


class TypeJob(models.Model):
    name = models.CharField(max_length=64, verbose_name='问题类型', unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "问题类型"
        verbose_name_plural = verbose_name


class JobDetail(models.Model):
    createTime = models.DateTimeField(verbose_name="创建时间", default=timezone.now)
    username = models.ForeignKey(to="basedata.UserInfo", verbose_name="提交人", to_field='name', null=True, blank=True,
                                 on_delete=models.CASCADE)
    typejobs = models.ForeignKey(to="TypeJob", verbose_name="问题类型", to_field='name', null=True, blank=True,
                                 on_delete=models.CASCADE)
    note = models.TextField(verbose_name='问题描述', default=None)
    status = models.BooleanField(verbose_name='完成状态', default=True)
    jobuser = models.CharField(max_length=32, verbose_name='维修人', choices=(
        ('hub', '胡兵'),
        ('admin', '管理员')
    ), default='胡兵')
    timeEnd = models.DateTimeField(verbose_name='更新时间', auto_now_add=timezone.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'createTime': self.createTime.strftime('%Y-%m-%d'),
            'username': self.username.name,
            'typejobs': self.typejobs.name,
            'note': self.note,
            'status': self.status,
            'jobuser': self.jobuser,
        }
    
    def __str__(self):
        return self.typejobs.name
    
    class Meta:
        ordering = ['-id']
        verbose_name = "日常工作"
        verbose_name_plural = verbose_name


class JobWorks(models.Model):
    crente_time = models.DateField(verbose_name='申请日期', auto_created=timezone.now)
    start_time = models.DateField(verbose_name='采购日期', auto_created=timezone.now)
    name = models.CharField(max_length=128, verbose_name='采购名称')
    type = models.CharField(max_length=32, verbose_name='采购来源', choices=(
        ('京东', '京东'),
        ('淘宝', '淘宝'),
    ), default='淘宝')
    wuliu_name = models.CharField(max_length=32, verbose_name='物流公司', choices=(
        ('中国邮政', '中国邮政'),
        ('申通快递', '申通快递'),
        ('圆通快递', '圆通快递'),
        ('顺丰快递', '顺丰快递'),
        ('天天快递', '天天快递'),
        ('韵达快递', '韵达快递'),
        ('中通快递', '中通快递'),
        ('汇通快递', '汇通快递'),
    ), default='')
    name_id = models.CharField(max_length=128, verbose_name='快递单号', )
    status = models.BooleanField(verbose_name='是否签收', default=False)
    note = models.TextField(verbose_name='备注', default='←详情请点单号')
    
    def __str__(self):
        return self.name_id
    
    class Meta:
        verbose_name = "物流信息表"
        verbose_name_plural = verbose_name
