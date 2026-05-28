from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import Track, Genre
from .serializers import TrackSerializer, GenreSerializer
from users.models import ArtistProfile
from users.artist_serializers import PublicArtistProfileSerializer
from releases.models import Release
from releases.serializers import PublicReleaseSerializer


class SearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '')
        search_type = request.query_params.get('type', 'all')

        if not query:
            return Response(
                {'error': 'Please provide a search query!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = {}

        # Search tracks
        if search_type in ['all', 'tracks']:
            tracks = Track.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query),
                visibility='public'
            )
            results['tracks'] = TrackSerializer(
                tracks, many=True
            ).data

        # Search artists
        if search_type in ['all', 'artists']:
            artists = ArtistProfile.objects.filter(
                Q(artist_name__icontains=query) |
                Q(bio__icontains=query)
            )
            results['artists'] = PublicArtistProfileSerializer(
                artists, many=True
            ).data

        # Search releases
        if search_type in ['all', 'releases']:
            releases = Release.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query),
                visibility='public'
            )
            results['releases'] = PublicReleaseSerializer(
                releases, many=True
            ).data

        # Search by genre
        if search_type in ['all', 'genres']:
            genres = Genre.objects.filter(
                Q(name__icontains=query)
            )
            results['genres'] = GenreSerializer(
                genres, many=True
            ).data

        return Response({
            'query': query,
            'type': search_type,
            'results': results
        })


class SearchTracksView(generics.ListAPIView):
    serializer_class = TrackSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        genre = self.request.query_params.get('genre', '')

        tracks = Track.objects.filter(visibility='public')

        if query:
            tracks = tracks.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        if genre:
            tracks = tracks.filter(
                release__genre__name__icontains=genre
            )

        return tracks


class SearchArtistsView(generics.ListAPIView):
    serializer_class = PublicArtistProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        artists = ArtistProfile.objects.all()

        if query:
            artists = artists.filter(
                Q(artist_name__icontains=query) |
                Q(bio__icontains=query)
            )

        return artists


class SearchReleasesView(generics.ListAPIView):
    serializer_class = PublicReleaseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        genre = self.request.query_params.get('genre', '')
        release_type = self.request.query_params.get('type', '')

        releases = Release.objects.filter(visibility='public')

        if query:
            releases = releases.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        if genre:
            releases = releases.filter(
                genre__name__icontains=genre
            )

        if release_type:
            releases = releases.filter(
                release_type=release_type
            )

        return releases
