from django.contrib import admin
from django.utils.translation import gettext_lazy

from web import models

# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'image_data', 'mobile', 'username', 'email','vip']

    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),
    
        (gettext_lazy('用户扩展信息'), {'fields': ('mobile', 'nickname', 'aravtr', 'vip')}),
    
        (gettext_lazy('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active',
                                                  'groups', 'user_permissions')}),
    
        (gettext_lazy('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
