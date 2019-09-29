from django.db import models
# Create your models here.
from django.utils import timezone

from basedata.models import UserInfo


class ModelName(models.Model):
    name = models.CharField(max_length=32, verbose_name='设备名称', unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "设备名称"
        verbose_name_plural = verbose_name


class ModelType(models.Model):
    name = models.CharField(max_length=32, verbose_name='耗材名称', unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "耗材名称"
        verbose_name_plural = verbose_name


class Prints(models.Model):
    userinfo = models.ForeignKey(to="basedata.UserInfo", verbose_name='申请人', to_field='name', on_delete=models.CASCADE)
    model_name = models.ForeignKey(to="ModelName", on_delete=models.CASCADE, null=True, blank=True, to_field='name',
                                   verbose_name="设备名称")
    model_name_type = models.ForeignKey(to="ModelType", on_delete=models.CASCADE, null=True, blank=True,
                                        to_field='name', verbose_name='耗材名称')
    add_times = models.DateField(verbose_name='申请时间', default=timezone.now)
    num = models.IntegerField(verbose_name='申请数量', default=1)
    addr = models.CharField(max_length=32, verbose_name='所在地区', default='松江')
    note = models.CharField(max_length=255, verbose_name='备注', default='无')
    
    def to_dict(self):
        return {
            'id': self.id,
            'add_times': self.add_times.strftime('%Y-%m-%d'),
            'userinfo': self.userinfo.name,
            'model_name': self.model_name.name,
            'model_name_type': self.model_name_type.name,
            'num': self.num,
            'addr': self.addr,
            'note': self.note,
        }
    
    class Meta:
        verbose_name = "打印耗材"
        verbose_name_plural = verbose_name
