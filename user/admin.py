from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import CustomUser
from django.utils.html import format_html


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'age', 'blood_group', 'gender', 'is_active',
    )
    list_filter = ('blood_group', 'gender', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'blood_group')
    ordering = ('username',)

    fieldsets = (
        ('Login & Permissions', {
            'fields': (
                'username', 'email', 'password',
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions',
            )
        }),
        ('Personal Info', {                         # ✅ first_name, last_name added
            'fields': (
                'first_name', 'last_name',
                'age', 'address', 'blood_group', 'gender',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email',
                'first_name', 'last_name',
                'password1', 'password2',
                'age', 'address', 'blood_group', 'gender',
                'is_active', 'is_staff',
            ),
        }),
    )
