from django.contrib import admin
from .models import Release

@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'release_type', 'visibility', 'created_at']
    list_filter = ['release_type', 'visibility']
    search_fields = ['title', 'artist__artist_name']
