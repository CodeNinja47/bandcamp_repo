# Create your models here.
from django.db import models
from users.models import ArtistProfile
from music.models import Genre, Track
from users.validators import validate_title_word_count

# ─────────────────────────────
# RELEASE MODEL
# ─────────────────────────────
class Release(models.Model):
    class ReleaseType(models.TextChoices):
        ALBUM = 'album', 'Album'
        EP = 'ep', 'EP'
        SINGLE = 'single', 'Single'

    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Public'
        PRIVATE = 'private', 'Private'

    artist = models.ForeignKey(
        ArtistProfile,
        on_delete=models.CASCADE,    # artist deleted → releases deleted
        related_name='releases'
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
    release_type = models.CharField(
        max_length=10,
        choices=ReleaseType.choices,
        default=ReleaseType.ALBUM
    )
    release_date = models.DateField(
        null=True,
        blank=True
    )
    cover_artwork = models.ImageField(
        upload_to='cover_artwork/',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='releases',
        blank=True
    )
    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PRIVATE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'releases_release'
        constraints = [
            # Same artist cannot have 2 releases with same title
            models.UniqueConstraint(
                fields=['artist', 'title'],
                name='unique_release_per_artist'
            ),
            models.CheckConstraint(
                condition=models.Q(
                    release_type__in=['album', 'ep', 'single']
                ),
                name='release_type_choices'
            ),
            models.CheckConstraint(
                condition=models.Q(
                    visibility__in=['public', 'private']
                ),
                name='release_visibility_choices'
            )
        ]

    def __str__(self):
        return f"{self.artist.artist_name} - {self.title}"
