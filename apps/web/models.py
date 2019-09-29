from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.utils.html import format_html


class User(AbstractUser):
    mobile = models.CharField(max_length=32, verbose_name='手机号', null=True, blank=True, default='13838389428')
    nickname = models.CharField(max_length=32, verbose_name='用户昵称', default='Titan', null=True, blank=True)
    aravtr = models.ImageField(upload_to='user/%Y-%m-%d', default='image/default.png', max_length=100,
                               verbose_name='用户头像')
    vip = models.CharField(max_length=10, verbose_name='用户身份', choices=(
        ('员工', '员工'),
        ('经理', '经理'),
        ('总监', '总监'),
    ))
    
    def image_data(self):
        return format_html(
            '<img src="/media/{}" style="width: 60px;height: 60px"/>',
            self.aravtr,
        )
    
    image_data.short_description = '用户头像'
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name
