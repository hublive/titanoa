from django.db import models

# Create your models here.
from basedata.models import *


class Inventory(models.Model):
    org = models.ForeignKey(to="basedata.Organization", on_delete=models.CASCADE, verbose_name='供应商')
    warehouse = models.ForeignKey(to="basedata.Warehouse", on_delete=models.CASCADE, verbose_name='所属仓库')
    material = models.ForeignKey(to="basedata.Material", on_delete=models.CASCADE, verbose_name='物品信息')
    measure = models.ForeignKey(to="basedata.Measure", on_delete=models.CASCADE, verbose_name='单位')
    cnt = models.DecimalField(verbose_name="库存数量", max_digits=14, decimal_places=2)

    def sumPrice(self):
        return self.cnt * self.material.stock_price

    sumPrice.short_description = u'总价'

    def __str__(self):
        return self.material.name

    class Meta:
        verbose_name = "库存信息"
        verbose_name_plural = verbose_name
