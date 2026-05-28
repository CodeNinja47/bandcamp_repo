# Register your models here.
from django.contrib import admin
from .models import Track, TrackFile, Genre, ProcessingJob

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'release', 'transcoding_status', 'visibility', 'upload_timestamp']
    list_filter = ['transcoding_status', 'visibility']
    search_fields = ['title']

@admin.register(TrackFile)
class TrackFileAdmin(admin.ModelAdmin):
    list_display = ['track', 'format', 'bitrate', 'file_size']
    list_filter = ['format']

@admin.register(ProcessingJob)
class ProcessingJobAdmin(admin.ModelAdmin):
    list_display = ['track', 'format', 'status', 'retries', 'created_at']
    list_filter = ['status', 'format']
