from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import SignUpUserForm


class UserRegAdmin(UserAdmin):
    """Регистрация модели User в админке"""
    add_form = SignUpUserForm
    list_display = 'email', 'is_superuser', 'is_staff', 'is_active',
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('персональная информация'),
         {'fields': ('username', 'first_name', 'last_name', 'surname', 'phone_number', 'photo',)}),
        (
            _('разрешения'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('важные даты'), {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2',),
            },
        ),
    )
    ordering = '-is_superuser', '-is_staff',
    search_fields = ("username",)


admin.site.register(get_user_model(), UserRegAdmin)
