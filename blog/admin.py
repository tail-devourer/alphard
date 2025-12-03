from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import User, CustomGroup


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("full_name", "avatar")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("full_name", "username", "email", "usable_password", "password1", "password2"),
        }),
    )
    list_display = ("username", "email", "full_name", "is_staff")
    search_fields = ("username", "full_name", "email")


admin.site.unregister(Group)

admin.site.register(User, CustomUserAdmin)
admin.site.register(CustomGroup, GroupAdmin)
