import subprocess
import json

def extract_video_metadata(video_path):
    try:
        # Run ffprobe command to get video metadata
        command = [
            'ffprobe', 
            '-v', 'error', 
            '-show_entries', 'format=duration,bit_rate', 
            '-show_entries', 'stream=codec_name,codec_type,width,height,r_frame_rate',
            '-of', 'json', 
            video_path
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        metadata = json.loads(result.stdout)
        return metadata
    except Exception as e:
        print(f"Error extracting video metadata: {e}")
        return {}

# Example usage
video_path = 'meta/output.mp4'
metadata = extract_video_metadata(video_path)
print(json.dumps(metadata, indent=4))
