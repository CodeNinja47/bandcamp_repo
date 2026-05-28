from django.urls import path
from .views import (
    GenreListView,
    TrackListView,
    TrackUploadView,
    TrackDetailView,
    TrackFileListView,
    ProcessingJobListView,
    PublicTrackListView,
    TrackMetadataView
)

urlpatterns = [
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('tracks/upload/', TrackUploadView.as_view(), name='track-upload'),
    path('tracks/<int:pk>/', TrackDetailView.as_view(), name='track-detail'),
    path('tracks/<int:pk>/metadata/', TrackMetadataView.as_view(), name='track-metadata'),
    path('tracks/<int:track_id>/files/', TrackFileListView.as_view(), name='track-files'),
    path('tracks/<int:track_id>/jobs/', ProcessingJobListView.as_view(), name='track-jobs'),
    path('public/tracks/', PublicTrackListView.as_view(), name='public-tracks'),
]
