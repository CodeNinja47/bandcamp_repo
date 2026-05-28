import subprocess
import os
from celery import shared_task
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def transcode_audio(self, track_id, format):
    from .models import Track, TrackFile, ProcessingJob

    try:
        track = Track.objects.get(id=track_id)
        job = ProcessingJob.objects.get(
            track=track,
            format=format
        )

        # Update status to processing
        job.status = 'processing'
        job.save()

        # Input file path
        input_path = track.original_file.path

        # Output file path
        output_dir = os.path.join(
            settings.MEDIA_ROOT,
            'tracks',
            'transcoded'
        )
        os.makedirs(output_dir, exist_ok=True)

        output_filename = f"track_{track_id}_{format}.{format}"
        output_path = os.path.join(output_dir, output_filename)

        # FFmpeg command based on format
        if format == 'mp3':
            command = [
                'ffmpeg', '-i', input_path,
                '-codec:a', 'libmp3lame',
                '-b:a', '320k',
                '-y', output_path
            ]
        elif format == 'aac':
            command = [
                'ffmpeg', '-i', input_path,
                '-codec:a', 'aac',
                '-b:a', '256k',
                '-y', output_path
            ]
        elif format == 'ogg':
            command = [
                'ffmpeg', '-i', input_path,
                '-codec:a', 'libvorbis',
                '-b:a', '192k',
                '-y', output_path
            ]

        # Run FFmpeg
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"FFmpeg error: {result.stderr}")

        # Get file size
        file_size = os.path.getsize(output_path)

        # Get metadata of transcoded file
        from .metadata import extract_metadata
        metadata = extract_metadata(output_path)

        # Save track file
        relative_path = os.path.relpath(
            output_path,
            settings.MEDIA_ROOT
        )
        TrackFile.objects.create(
            track=track,
            file=relative_path,
            format=format,
            file_size=file_size,
            bitrate=metadata.get('bitrate') if metadata else None,
            sample_rate=metadata.get('sample_rate') if metadata else None,
            codec=metadata.get('codec') if metadata else None
        )

        # Update job status
        job.status = 'completed'
        job.save()

        # Check if all jobs completed
        all_jobs = ProcessingJob.objects.filter(track=track)
        if all_jobs.filter(status='completed').count() == all_jobs.count():
            track.transcoding_status = 'completed'
            track.save()

        return f"Successfully transcoded track {track_id} to {format}"

    except Exception as exc:
        job = ProcessingJob.objects.get(
            track_id=track_id,
            format=format
        )
        job.status = 'failed'
        job.error_log = str(exc)
        job.retries += 1
        job.save()

        track = Track.objects.get(id=track_id)
        track.transcoding_status = 'failed'
        track.save()

        raise self.retry(exc=exc, countdown=60)


@shared_task
def extract_track_metadata(track_id):
    """
    Extract and save metadata from uploaded track
    """
    from .models import Track
    from .metadata import extract_metadata

    try:
        track = Track.objects.get(id=track_id)
        file_path = track.original_file.path

        metadata = extract_metadata(file_path)

        if metadata:
            # Update track with metadata
            track.duration = metadata.get('duration')
            track.file_size = metadata.get('file_size')
            track.save()

        return f"Metadata extracted for track {track_id}"

    except Exception as e:
        return f"Error extracting metadata: {e}"
