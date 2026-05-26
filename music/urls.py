from django.urls import path
from .views import (
    GenreListView,
    TrackListView,
    TrackUploadView,
    TrackDetailView,
    TrackFileListView,
    ProcessingJobListView,
    PublicTrackListView
)

urlpatterns = [
    # Genre endpoints
    path('genres/', GenreListView.as_view(), name='genre-list'),

    # Track endpoints
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('tracks/upload/', TrackUploadView.as_view(), name='track-upload'),
    path('tracks/<int:pk>/', TrackDetailView.as_view(), name='track-detail'),
    path('tracks/<int:track_id>/files/', TrackFileListView.as_view(), name='track-files'),
    path('tracks/<int:track_id>/jobs/', ProcessingJobListView.as_view(), name='track-jobs'),

    # Public endpoints
    path('public/tracks/', PublicTrackListView.as_view(), name='public-tracks'),
]
