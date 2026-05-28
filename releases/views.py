from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from .models import Release
from music.models import Track
from .serializers import (
    ReleaseSerializer,
    ReleaseCreateSerializer,
    PublicReleaseSerializer,
    AddTrackToReleaseSerializer
)


class ReleaseListView(generics.ListAPIView):
    serializer_class = ReleaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Release.objects.all()
        try:
            artist_profile = user.artist_profile
            return Release.objects.filter(artist=artist_profile)
        except:
            return Release.objects.none()


class ReleaseCreateView(generics.CreateAPIView):
    serializer_class = ReleaseCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def create(self, request, *args, **kwargs):
        # Only artists can create releases
        if request.user.role != 'artist':
            return Response(
                {'error': 'Only artists can create releases!'},
                status=status.HTTP_403_FORBIDDEN
            )
        # Check if artist has a profile
        if not hasattr(request.user, 'artist_profile'):
            return Response(
                {'error': 'Please create an artist profile first!'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)


class ReleaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReleaseSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Release.objects.all()
        try:
            artist_profile = user.artist_profile
            return Release.objects.filter(artist=artist_profile)
        except:
            return Release.objects.none()


class AddTrackToReleaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        release = get_object_or_404(Release, pk=pk)
        serializer = AddTrackToReleaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        track_id = serializer.validated_data['track_id']
        track = get_object_or_404(Track, id=track_id)
        # Add track to release
        track.release = release
        track.save()
        return Response(
            {'message': 'Track added to release successfully!'},
            status=status.HTTP_200_OK
        )


class RemoveTrackFromReleaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        release = get_object_or_404(Release, pk=pk)
        serializer = AddTrackToReleaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        track_id = serializer.validated_data['track_id']
        track = get_object_or_404(Track, id=track_id)
        # Remove track from release
        track.release = None
        track.save()
        return Response(
            {'message': 'Track removed from release successfully!'},
            status=status.HTTP_200_OK
        )


class PublishReleaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        release = get_object_or_404(Release, pk=pk)
        release.visibility = 'public'
        release.save()
        return Response(
            {'message': 'Release published successfully!'},
            status=status.HTTP_200_OK
        )


class UnpublishReleaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        release = get_object_or_404(Release, pk=pk)
        release.visibility = 'private'
        release.save()
        return Response(
            {'message': 'Release unpublished successfully!'},
            status=status.HTTP_200_OK
        )


class PublicReleaseListView(generics.ListAPIView):
    serializer_class = PublicReleaseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Release.objects.filter(visibility='public')


class PublicReleaseDetailView(generics.RetrieveAPIView):
    serializer_class = PublicReleaseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Release.objects.filter(visibility='public')
