from rest_framework import serializers
from .models import Track, TrackFile, Genre, ProcessingJob
from users.validators import validate_audio_file_size, validate_audio_format

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id']

class TrackFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackFile
        fields = [
            'id', 'track', 'file', 'format',
            'bitrate', 'file_size', 'sample_rate',
            'codec', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class ProcessingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingJob
        fields = [
            'id', 'track', 'status', 'format',
            'error_log', 'retries', 'max_retries',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class TrackSerializer(serializers.ModelSerializer):
    track_files = TrackFileSerializer(many=True, read_only=True)
    processing_jobs = ProcessingJobSerializer(many=True, read_only=True)

    class Meta:
        model = Track
        fields = [
            'id', 'release', 'title', 'description',
            'duration', 'track_number', 'original_file',
            'file_size', 'transcoding_status', 'visibility',
            'upload_timestamp', 'track_files', 'processing_jobs'
        ]
        read_only_fields = [
            'id', 'upload_timestamp',
            'transcoding_status', 'file_size', 'duration'
        ]

    def validate_original_file(self, value):
        validate_audio_file_size(value)
        validate_audio_format(value)
        return value

class TrackUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = [
            'id', 'title', 'description',
            'track_number', 'original_file', 'visibility'
        ]
        read_only_fields = ['id']

    def validate_original_file(self, value):
        validate_audio_file_size(value)
        validate_audio_format(value)
        return value

    def create(self, validated_data):
        audio_file = validated_data.get('original_file')
        if audio_file:
            validated_data['file_size'] = audio_file.size
        return super().create(validated_data)
