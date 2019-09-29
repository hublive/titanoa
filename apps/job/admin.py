from django.contrib import admin

from job import models


# Register your models here.
@admin.register(models.TypeJob)
class TypeJobConfig(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.JobDetail)
class JobDetailConfig(admin.ModelAdmin):
    list_display = ['createTime', 'username', 'typejobs', 'note', 'status', 'jobuser', 'timeEnd']
    raw_id_fields = ("username",)
    search_fields = ['typejobs', 'username']
    list_filter = ['typejobs', 'username']
    list_per_page = 10


@admin.register(models.JobWorks)
class JobWorksConfig(admin.ModelAdmin):
    list_display = ['crente_time', 'start_time', 'name', 'type', 'name_id', 'wuliu_name', 'status', 'note']
    list_editable = ['name_id', 'status']
    # raw_id_fields = ("username", )
