from django.core.exceptions import ValidationError
import os

# Bio word count validator
def validate_bio_word_count(value):
    words = value.split()
    if len(words) > 100:
        raise ValidationError(
            'Bio cannot exceed 100 words! '
            f'Current word count: {len(words)}'
        )

# Profile image validator
def validate_profile_image(image):
    # Check file size (5MB limit)
    if image.size > 5 * 1024 * 1024:
        raise ValidationError('Image size cannot exceed 5MB!')
    
    # Check file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(
            'Only JPG, PNG, WEBP images allowed!'
        )

# Audio file size validator
def validate_audio_file_size(file):
    if file.size > 500 * 1024 * 1024:  # 500MB
        raise ValidationError(
            'Audio file cannot exceed 500MB!'
        )

# Audio file format validator
def validate_audio_format(file):
    valid_extensions = ['.wav', '.mp3', '.flac', '.aiff']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(
            'Only WAV, MP3, FLAC, AIFF files allowed!'
        )

# Title word count validator
def validate_title_word_count(value):
    words = value.split()
    if len(words) > 100:
        raise ValidationError(
            'Title cannot exceed 100 words!'
        )
