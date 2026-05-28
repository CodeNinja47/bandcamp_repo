from rest_framework import serializers
from .models import ArtistProfile
from .validators import validate_bio_word_count, validate_profile_image


class ArtistProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ArtistProfile
        fields = [
            'id', 'email', 'username', 'artist_name',
            'bio', 'profile_image', 'social_links', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'email', 'username']

    def validate_bio(self, value):
        validate_bio_word_count(value)
        return value

    def validate_profile_image(self, value):
        validate_profile_image(value)
        return value


class ArtistProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistProfile
        fields = [
            'artist_name', 'bio',
            'profile_image', 'social_links'
        ]

    def validate_bio(self, value):
        validate_bio_word_count(value)
        return value

    def validate_profile_image(self, value):
        if value:
            validate_profile_image(value)
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        # Check if profile already exists
        if ArtistProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                'Artist profile already exists!'
            )
        # Check if user is artist
        if user.role != 'artist':
            raise serializers.ValidationError(
                'Only artists can create an artist profile!'
            )
        return ArtistProfile.objects.create(
            user=user,
            **validated_data
        )


class PublicArtistProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ArtistProfile
        fields = [
            'id', 'username', 'artist_name',
            'bio', 'profile_image', 'social_links',
            'created_at'
        ]
        read_only_fields = fields
