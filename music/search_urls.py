from django.urls import path
from .search_views import (
    SearchView,
    SearchTracksView,
    SearchArtistsView,
    SearchReleasesView
)

urlpatterns = [
    path('', SearchView.as_view(), name='search'),
    path('tracks/', SearchTracksView.as_view(), name='search-tracks'),
    path('artists/', SearchArtistsView.as_view(), name='search-artists'),
    path('releases/', SearchReleasesView.as_view(), name='search-releases'),
]
