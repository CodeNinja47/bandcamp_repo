from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ArtistProfile

class CustomUserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'role', 'is_staff']
    search_fields = ['email', 'username']
    ordering = ['email']

admin.site.register(User, CustomUserAdmin)
admin.site.register(ArtistProfile)
