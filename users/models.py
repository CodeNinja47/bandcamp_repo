from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import (
    validate_bio_word_count,
    validate_profile_image
)

# ─────────────────────────────
# USER MODEL
# ─────────────────────────────
class User(AbstractUser):
    class Role(models.TextChoices):
        ARTIST = 'artist', 'Artist'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        null=False,
        blank=False
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.ARTIST,
        null=False,
        blank=False
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    password_reset_token = models.CharField(
    max_length=50,
    null=True,
    blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users_user'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(role__in=['artist', 'admin']),
                name='role_choices'
            )
        ]

    def __str__(self):
        return self.email


# ─────────────────────────────
# ARTIST PROFILE MODEL
# ─────────────────────────────
class ArtistProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,    # user deleted → profile deleted
        related_name='artist_profile'
    )
    artist_name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    bio = models.TextField(
        blank=True,
        null=True,
        validators=[validate_bio_word_count]
    )
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        validators=[validate_profile_image]
    )
    social_links = models.JSONField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_artistprofile'

    def clean(self):
        if self.user.role != 'artist':
            from django.core.exceptions import ValidationError
            raise ValidationError(
                'Only users with artist role can have an artist profile!'
            )

    def __str__(self):
        return f"{self.artist_name} - {self.user.email}"
