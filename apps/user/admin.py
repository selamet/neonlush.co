from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.user.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin interface for custom User model."""
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields': ('phone_number', 'tag')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {'fields': ('phone_number', 'tag')}),
    )
    list_display = UserAdmin.list_display + ('phone_number', 'tag')
    list_filter = UserAdmin.list_filter + ('tag',)
