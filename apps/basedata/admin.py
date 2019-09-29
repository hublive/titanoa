from django.contrib import admin

# Register your models here.
from basedata import models


@admin.register(models.UserInfo)
class UserConfig(admin.ModelAdmin):
    list_display = ['name', 'dept']
    search_fields = ['name', 'dept']


@admin.register(models.Warehouse)
class WarehouseConfig(admin.ModelAdmin):
    list_display = ['code', 'name', 'location']
    # filter_horizontal = ('users')


@admin.register(models.Measure)
class MeasureConfig(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Brand)
class BrandConfig(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Category)
class CategoryConfig(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Material)
class MaterialConfig(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'image_data', 'spec', 'brand', 'category', 'warehouse',
                    'stock_price']
    
    # list_editable = ['code']


@admin.register(models.Organization)
class OrganizationConfig(admin.ModelAdmin):
    list_display = ['name', 'users', 'type', 'phone', 'addr', 'status', 'note']
    raw_id_fields = ("users",)


@admin.register(models.Computer)
class ComputerConfig(admin.ModelAdmin):
    list_display = ['name', 'type', 'mainboard', 'CPU', 'memory', 'disk', 'video', 'displayer']
    list_per_page = 8
    search_fields = ['name']
    list_filter = ['type']


@admin.register(models.Property)
class PropertyConfig(admin.ModelAdmin):
    list_display = ['p_id', 'p_name', 'p_brand', 'p_sn', 'p_price',
                    'image_data', 'p_status', 'p_organization', 'p_user', 'p_computers',
                    'p_time']
    
    raw_id_fields = ("p_user", 'p_computers', 'p_brand',)
    list_editable = ['p_status', 'p_user']
    search_fields = ['p_id', 'p_name']
    list_per_page = 10
    list_filter = ['p_name','p_status']
