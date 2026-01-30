from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import CustomUser, CustomGroup


class CustomUserAdmin(UserAdmin):
    """fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'username', 'email', 'usable_password', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'username', 'email', 'full_name', 'is_staff')
    search_fields = ('id', 'username', 'full_name', 'email')"""
    pass


admin.site.unregister(Group)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomGroup, GroupAdmin)
