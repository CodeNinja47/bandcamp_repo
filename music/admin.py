from django.contrib import admin
from .models import Track, TrackFile, Genre, ProcessingJob


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    actions = ['delete_selected']


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'transcoding_status', 'visibility', 'upload_timestamp']
    list_filter = ['transcoding_status', 'visibility']
    search_fields = ['title']
    actions = ['delete_selected']


@admin.register(TrackFile)
class TrackFileAdmin(admin.ModelAdmin):
    list_display = ['track', 'format', 'bitrate', 'file_size']
    list_filter = ['format']
    actions = ['delete_selected']


@admin.register(ProcessingJob)
class ProcessingJobAdmin(admin.ModelAdmin):
    list_display = ['track', 'format', 'status', 'retries', 'created_at']
    list_filter = ['status', 'format']
    actions = ['delete_selected']
