import subprocess

# Allowed extensions
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'avi', 'mov', 'mp4', 'opus', 'ogg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to extract audio from video
def extract_audio_from_video(video_path: str, audio_output_path: str) -> None:
    command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-i', video_path,
        '-vn',  # Disable video
        '-acodec', 'pcm_s16le',  # Audio codec
        '-ar', '44100',  # Sampling rate
        '-ac', '2',  # Number of channels
        audio_output_path
    ]
    subprocess.run(command, check=True)