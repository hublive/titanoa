from django.contrib import admin

# Register your models here.

from invent import models


@admin.register(models.Inventory)
class InventoryConfig(admin.ModelAdmin):
    list_display = ['org', 'warehouse', 'material', 'measure', 'cnt', 'sumPrice']
    raw_id_fields = ("warehouse",'material',)
    list_editable = ['cnt']
    list_filter = ['warehouse']
    search_fields = ['material__name']
