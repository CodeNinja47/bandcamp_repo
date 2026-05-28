import subprocess
import json
import os


def extract_metadata(file_path):
    """
    Extract metadata from audio file using ffprobe
    """
    try:
        command = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            file_path
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"ffprobe error: {result.stderr}")

        data = json.loads(result.stdout)

        # Extract audio stream info
        audio_stream = None
        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'audio':
                audio_stream = stream
                break

        format_info = data.get('format', {})

        metadata = {
            'duration': float(format_info.get('duration', 0)),
            'bitrate': int(format_info.get('bit_rate', 0)),
            'file_size': int(format_info.get('size', 0)),
            'format_name': format_info.get('format_name', ''),
        }

        if audio_stream:
            metadata.update({
                'sample_rate': int(audio_stream.get('sample_rate', 0)),
                'codec': audio_stream.get('codec_name', ''),
                'channels': int(audio_stream.get('channels', 0)),
            })

        return metadata

    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return None


def get_audio_duration(file_path):
    """
    Get duration of audio file in seconds
    """
    metadata = extract_metadata(file_path)
    if metadata:
        return metadata.get('duration', 0)
    return 0


def get_audio_bitrate(file_path):
    """
    Get bitrate of audio file
    """
    metadata = extract_metadata(file_path)
    if metadata:
        return metadata.get('bitrate', 0)
    return 0
