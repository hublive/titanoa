from django.contrib import admin

from itcomputer import models


# Register your models here.
@admin.register(models.Check)
class CheckConfig(admin.ModelAdmin):
    list_display = ['c_company', 'c_time', 'c_property', 'c_num', 'c_caigou_name',
                    'c_ghs_id', 'c_ysbg_wg', 'c_ysbg_jl', 'c_ysr_name']
    raw_id_fields = ("c_property",)


@admin.register(models.BaoFei)
class BaoFeiConfig(admin.ModelAdmin):
    list_display = ['b_time', 'b_userinfo', 'b_ids', 'b_way', 'b_num',
                    'b_note']
    raw_id_fields = ("b_ids", 'b_userinfo',)


@admin.register(models.FixedAssets)
class FixedAssetsConfig(admin.ModelAdmin):
    list_display = ['f_time', 'f_property', 'f_addr', 'f_note']
    raw_id_fields = ("f_property",)
    list_per_page = 10
    list_display_links = ['f_time','f_property']


@admin.register(models.Equipment)
class EquipmentConfig(admin.ModelAdmin):
    list_display = ['add_time', 'type', 'propertys', 'model_name', 'model_type',
                    'model_num', 'model_price', 'model_username','note']
    raw_id_fields = ("propertys", 'model_type',)
