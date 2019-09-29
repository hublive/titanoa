from django.contrib import admin

# Register your models here.
from prints import models


@admin.register(models.ModelName)
class ModelNameConfig(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(models.ModelType)
class ModelTypeConfig(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(models.Prints)
class PrintsConfig(admin.ModelAdmin):
    list_display = ['userinfo', 'model_name', 'model_name_type', 'add_times', 'num', 'addr', 'note']
    search_fields = ['userinfo__name', 'model_name__name', 'model_name_type__name', 'addr']
    raw_id_fields = ['userinfo']
    list_filter = ['userinfo']
