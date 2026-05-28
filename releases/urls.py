from django.urls import path
from .views import (
    ReleaseListView,
    ReleaseCreateView,
    ReleaseDetailView,
    AddTrackToReleaseView,
    RemoveTrackFromReleaseView,
    PublishReleaseView,
    UnpublishReleaseView,
    PublicReleaseListView,
    PublicReleaseDetailView
)

urlpatterns = [
    # Artist release endpoints
    path('', ReleaseListView.as_view(), name='release-list'),
    path('create/', ReleaseCreateView.as_view(), name='release-create'),
    path('<int:pk>/', ReleaseDetailView.as_view(), name='release-detail'),
    path('<int:pk>/add-track/', AddTrackToReleaseView.as_view(), name='release-add-track'),
    path('<int:pk>/remove-track/', RemoveTrackFromReleaseView.as_view(), name='release-remove-track'),
    path('<int:pk>/publish/', PublishReleaseView.as_view(), name='release-publish'),
    path('<int:pk>/unpublish/', UnpublishReleaseView.as_view(), name='release-unpublish'),

    # Public endpoints
    path('public/', PublicReleaseListView.as_view(), name='public-release-list'),
    path('public/<int:pk>/', PublicReleaseDetailView.as_view(), name='public-release-detail'),
]
