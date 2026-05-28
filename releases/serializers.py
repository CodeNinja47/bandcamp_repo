from rest_framework import serializers
from .models import Release
from music.serializers import TrackSerializer
from users.models import ArtistProfile


class ReleaseSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    artist_name = serializers.CharField(
        source='artist.artist_name',
        read_only=True
    )

    class Meta:
        model = Release
        fields = [
            'id', 'artist', 'artist_name', 'title',
            'description', 'release_type', 'release_date',
            'cover_artwork', 'genre', 'visibility',
            'created_at', 'updated_at', 'tracks'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'artist']


class ReleaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = [
            'id', 'title', 'description', 'release_type',
            'release_date', 'cover_artwork', 'genre', 'visibility'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        # Check if user has artist profile
        try:
            artist_profile = user.artist_profile
        except ArtistProfile.DoesNotExist:
            raise serializers.ValidationError(
                'Please create an artist profile first!'
            )
        # Handle ManyToMany genre field
        genre = validated_data.pop('genre', [])
        release = Release.objects.create(
            artist=artist_profile,
            **validated_data
        )
        release.genre.set(genre)
        return release


class PublicReleaseSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    artist_name = serializers.CharField(
        source='artist.artist_name',
        read_only=True
    )

    class Meta:
        model = Release
        fields = [
            'id', 'artist_name', 'title', 'description',
            'release_type', 'release_date', 'cover_artwork',
            'genre', 'visibility', 'created_at', 'tracks'
        ]


class AddTrackToReleaseSerializer(serializers.Serializer):
    track_id = serializers.IntegerField()

    def validate_track_id(self, value):
        from music.models import Track
        try:
            Track.objects.get(id=value)
        except Track.DoesNotExist:
            raise serializers.ValidationError(
                'Track not found!'
            )
        return value
