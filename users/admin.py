from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ArtistProfile


class CustomUserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['email']
    actions = ['delete_selected']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )


class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ['artist_name', 'user', 'created_at']
    search_fields = ['artist_name', 'user__email']
    actions = ['delete_selected']


admin.site.register(User, CustomUserAdmin)
admin.site.register(ArtistProfile, ArtistProfileAdmin)
