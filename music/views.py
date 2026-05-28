from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import models
from .models import Track, TrackFile, Genre, ProcessingJob
from .serializers import (
    TrackSerializer,
    TrackUploadSerializer,
    TrackFileSerializer,
    ProcessingJobSerializer,
    GenreSerializer
)


class GenreListView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]


class TrackListView(generics.ListAPIView):
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Track.objects.all()
        try:
            artist_profile = user.artist_profile
            return Track.objects.filter(
                models.Q(release__artist=artist_profile) |
                models.Q(release__isnull=True)
            )
        except:
            return Track.objects.none()


class TrackUploadView(generics.CreateAPIView):
    serializer_class = TrackUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
    	track = serializer.save()
    	# Create processing jobs and trigger transcoding
    	for format in ['mp3', 'aac', 'ogg']:
        	ProcessingJob.objects.create(
            		track=track,
            		format=format,
            		status='pending'
        )
    # Trigger async transcoding
    	from .tasks import transcode_audio
    	for format in ['mp3', 'aac', 'ogg']:
        	transcode_audio.delay(track.id, format)
    	return track

    def create(self, request, *args, **kwargs):
        if request.user.role != 'artist':
            return Response(
                {'error': 'Only artists can upload tracks!'},
                status=status.HTTP_403_FORBIDDEN
            )
        if not hasattr(request.user, 'artist_profile'):
            return Response(
                {'error': 'Please create an artist profile first!'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)


class TrackDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Track.objects.all()
        try:
            artist_profile = user.artist_profile
            return Track.objects.filter(
                models.Q(release__artist=artist_profile) |
                models.Q(release__isnull=True)
            )
        except:
            return Track.objects.none()


class TrackFileListView(generics.ListAPIView):
    serializer_class = TrackFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        track_id = self.kwargs.get('track_id')
        return TrackFile.objects.filter(track_id=track_id)


class ProcessingJobListView(generics.ListAPIView):
    serializer_class = ProcessingJobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        track_id = self.kwargs.get('track_id')
        return ProcessingJob.objects.filter(track_id=track_id)


class PublicTrackListView(generics.ListAPIView):
    serializer_class = TrackSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Track.objects.filter(
            visibility='public',
            transcoding_status='completed'
        )
