from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/artists/', include('users.artist_urls')),
    path('api/music/', include('music.urls')),
    path('api/releases/', include('releases.urls')),
    path('api/search/', include('music.search_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
