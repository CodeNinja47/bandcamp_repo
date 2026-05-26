from django.urls import path
from .artist_views import (
    ArtistProfileCreateView,
    ArtistProfileDetailView,
    ArtistProfileDeleteView,
    PublicArtistListView,
    PublicArtistDetailView
)

urlpatterns = [
    # Artist own profile endpoints
    path('profile/create/', ArtistProfileCreateView.as_view(), name='artist-profile-create'),
    path('profile/', ArtistProfileDetailView.as_view(), name='artist-profile-detail'),
    path('profile/delete/', ArtistProfileDeleteView.as_view(), name='artist-profile-delete'),

    # Public endpoints
    path('', PublicArtistListView.as_view(), name='public-artist-list'),
    path('<int:pk>/', PublicArtistDetailView.as_view(), name='public-artist-detail'),
]
