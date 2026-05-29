from rest_framework import serializers
from .models import Release
from music.serializers import TrackSerializer
from users.models import ArtistProfile


class ReleaseSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(
        source='artist.artist_name',
        read_only=True
    )
    genre_names = serializers.SerializerMethodField()

    def get_genre_names(self, obj):
        return list(obj.genre.values_list('name', flat=True))

    def update(self, instance, validated_data):
        genre_names = validated_data.pop('genre_names', [])
        instance = super().update(instance, validated_data)
        if genre_names:
            instance.genre.clear()
            for genre_name in genre_names:
                from music.models import Genre
                genre, created = Genre.objects.get_or_create(
                    name=genre_name,
                    defaults={'slug': genre_name.lower().replace(' ', '-')}
                )
                instance.genre.add(genre)
        return instance

    class Meta:
        model = Release
        fields = [
            'id', 'artist', 'artist_name', 'title',
            'description', 'release_type', 'release_date',
            'cover_artwork', 'genre', 'genre_names',
            'visibility', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'artist']


class ReleaseCreateSerializer(serializers.ModelSerializer):
    genre_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Release
        fields = [
            'id', 'title', 'description', 'release_type',
            'release_date', 'cover_artwork', 'visibility',
            'genre_names'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            artist_profile = user.artist_profile
        except ArtistProfile.DoesNotExist:
            raise serializers.ValidationError(
                'Please create an artist profile first!'
            )

        # Handle genre names
        genre_names = validated_data.pop('genre_names', [])
        
        release = Release.objects.create(
            artist=artist_profile,
            **validated_data
        )

        # Get or create genres by name
        for genre_name in genre_names:
            from music.models import Genre
            genre, created = Genre.objects.get_or_create(
                name=genre_name,
                defaults={'slug': genre_name.lower().replace(' ', '-')}
            )
            release.genre.add(genre)

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
