# Create your models here.
from django.db import models
from users.models import ArtistProfile
from users.validators import (
    validate_audio_file_size,
    validate_audio_format,
    validate_title_word_count
)

# ─────────────────────────────
# GENRE MODEL
# ─────────────────────────────
class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        null=False,
        blank=False
    )

    class Meta:
        db_table = 'music_genre'
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(name=''),
                name='name_not_empty'
            )
        ]

    def __str__(self):
        return self.name


# ─────────────────────────────
# TRACK MODEL
# ─────────────────────────────
class Track(models.Model):
    class TranscodingStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Public'
        PRIVATE = 'private', 'Private'

    release = models.ForeignKey(
    'releases.Release',
    on_delete=models.SET_NULL,
    related_name='tracks',
    null=True,
    blank=True
    )
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        validators=[validate_title_word_count]
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    duration = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    track_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    original_file = models.FileField(
        upload_to='tracks/original/',
        validators=[
            validate_audio_file_size,
            validate_audio_format
        ]
    )
    file_size = models.BigIntegerField(
        null=True,
        blank=True
    )
    transcoding_status = models.CharField(
        max_length=20,
        choices=TranscodingStatus.choices,
        default=TranscodingStatus.PENDING
    )
    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PRIVATE
    )
    upload_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'music_track'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    transcoding_status__in=[
                        'pending', 'processing',
                        'completed', 'failed'
                    ]
                ),
                name='transcoding_status_choices'
            ),
            models.CheckConstraint(
                condition=models.Q(
                    file_size__lte=524288000  # 500MB
                ),
                name='file_size_limit'
            )
        ]

    def __str__(self):
        return self.title


# ─────────────────────────────
# TRACK FILE MODEL
# ─────────────────────────────
class TrackFile(models.Model):
    class Format(models.TextChoices):
        MP3 = 'mp3', 'MP3'
        AAC = 'aac', 'AAC'
        OGG = 'ogg', 'OGG'

    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,    # track deleted → files deleted
        related_name='track_files'
    )
    file = models.FileField(
        upload_to='tracks/transcoded/',
        null=False,
        blank=False
    )
    format = models.CharField(
        max_length=10,
        choices=Format.choices,
        null=False,
        blank=False
    )
    bitrate = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    file_size = models.BigIntegerField(
        null=True,
        blank=True
    )
    sample_rate = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    codec = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'music_trackfile'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(format__in=['mp3', 'aac', 'ogg']),
                name='trackfile_format_choices'
            )
        ]

    def __str__(self):
        return f"{self.track.title} - {self.format}"


# ─────────────────────────────
# PROCESSING JOB MODEL
# ─────────────────────────────
class ProcessingJob(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    class Format(models.TextChoices):
        MP3 = 'mp3', 'MP3'
        AAC = 'aac', 'AAC'
        OGG = 'ogg', 'OGG'

    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,    # track deleted → jobs deleted
        related_name='processing_jobs'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    format = models.CharField(
        max_length=10,
        choices=Format.choices,
        null=False,
        blank=False
    )
    error_log = models.TextField(
        blank=True,
        null=True
    )
    retries = models.PositiveIntegerField(default=0)
    max_retries = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'music_processingjob'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    status__in=[
                        'pending', 'processing',
                        'completed', 'failed'
                    ]
                ),
                name='processingjob_status_choices'
            ),
            models.CheckConstraint(
                condition=models.Q(max_retries__lte=5),
                name='max_retries_limit'
            ),
            models.CheckConstraint(
                condition=models.Q(retries__lte=models.F('max_retries')),
                name='retries_within_limit'
            )
        ]

    def can_retry(self):
        return self.retries < self.max_retries

    def __str__(self):
        return f"{self.track.title} - {self.format} - {self.status}"
