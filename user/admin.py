from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import CustomUser
from django.utils.html import format_html


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'username', 'email', 'age', 'blood_group', 'gender', 'is_available', 'last_donation_date', 'image_tag'
    )
    list_filter = ('blood_group', 'gender', 'is_available')
    search_fields = ('username', 'email', 'age', 'blood_group')
    ordering = ('username',)
    readonly_fields = ('image_tag',)

    fieldsets = (
        ('Login & Permissions', {'fields': ('username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Personal Info', {'fields': ('age', 'address', 'blood_group', 'gender', 'last_donation_date', 'is_available', 'image', 'image_tag')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'age', 'address', 'blood_group', 'gender', 'is_available', 'image'),
        }),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:50px;height:50px;border-radius:50%;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Profile Picture'