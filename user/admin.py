from django.contrib import admin
from user.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ["id", "username", 'is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', "is_superuser", 'user_permissions'),
        }),
        (_('Important dates'), {"fields": ('created_date',)})
    )