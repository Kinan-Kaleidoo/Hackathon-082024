import os

from flask import request, jsonify
import magic
from flask_login import login_required
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

# service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# client = storage.Client()
# buckets = list(client.list_buckets())
# for bucket in buckets:
#     print(bucket.name)

# Initialize Google Cloud Storage client
storage_client = storage.Client()
bucket_name = os.getenv('GOOGLE_CLOUD_BUCKET_NAME')
if not bucket_name:
    raise ValueError("Environment variable GOOGLE_CLOUD_BUCKET_NAME not set.")
bucket = storage_client.bucket(bucket_name)


def login():
    print()


@login_required
def index():
    print()


def media():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file:
            # Read the file content
            file_content = file.read()
            # Use python-magic to detect the file type from the file content
            mime = magic.Magic(mime=True)
            file_type = mime.from_buffer(file_content)
            # Check if the file type is an image or video
            if file_type.startswith('image/'):
                return serve_image(file)
            elif file_type.startswith('video/'):
                return serve_video(file)
            else:
                return jsonify({"error": "File is not an image or video", "media_type": file_type}), 400
        return jsonify({"error": "No file provided"}), 400
    else:
        # to add call from gallery to all his pictures or videos
        return jsonify("good"), 200


def serve_image(image):
    image.seek(0)
    public_url = upload_to_gcs(image, image.filename)
    return jsonify({"message": "File uploaded successfully", "file_url": public_url}), 200


def upload_to_gcs(file, destination_blob_name):
    """Uploads a file to the GCS bucket."""
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file)
    return blob.public_url


def serve_video(video):
    public_url = upload_to_gcs(video, video.filename)
    return jsonify({"message": "File uploaded successfully", "file_url": public_url}), 200


@login_required
def search():
    print()

@login_required
def doc():
    print()

@login_required
def audio():
    print()

@login_required
def video():
    print()
