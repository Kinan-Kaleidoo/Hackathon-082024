import os
import magic
from google.cloud import storage
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_login import login_required
from datetime import timedelta

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Initialize Google Cloud Storage client
storage_client = storage.Client()
bucket_name = os.getenv('GOOGLE_CLOUD_BUCKET_NAME')
if not bucket_name:
    raise ValueError("Environment variable GOOGLE_CLOUD_BUCKET_NAME not set.")
bucket = storage_client.bucket(bucket_name)

# Define allowed MIME types
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif"]
ALLOWED_VIDEO_TYPES = ["video/mp4", "video/quicktime", "video/x-msvideo", "video/x-matroska"]
ALLOWED_AUDIO_TYPES = ["audio/mpeg", "audio/wav", "audio/wave", "audio/x-wav", "audio/ogg"]
ALLOWED_TEXT_TYPES = ["text/plain", "application/octet-stream"]
ALLOWED_DOC_TYPES = ["application/pdf", "text/plain",
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]


def upload_file_to_gcs(file, destination_blob_name):
    """Uploads a file to a specific folder in a GCS bucket."""
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file, content_type=file.content_type)
    print(f"File uploaded to {destination_blob_name} in bucket {bucket_name}.")
    return blob.public_url


@login_required
def media():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Use python-magic to detect the file type
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file.read())
    file.seek(0)  # Reset file pointer after reading

    if file_type in ALLOWED_IMAGE_TYPES:
        destination_blob_name = f"media/images/{file.filename}"
    elif file_type in ALLOWED_VIDEO_TYPES:
        destination_blob_name = f"media/videos/{file.filename}"
    else:
        return jsonify({"error": "File is not an image or video", "file_type": file_type}), 400

    public_url = upload_file_to_gcs(file, destination_blob_name)
    return jsonify(
        {"message": "File uploaded successfully", "path": destination_blob_name, "file_url": public_url}), 200


@login_required
def doc():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Use python-magic to detect the file type
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file.read())
    file.seek(0)  # Reset file pointer after reading

    if file_type in ALLOWED_DOC_TYPES:
        destination_blob_name = f"docs/{file.filename}"
        public_url = upload_file_to_gcs(file, destination_blob_name)
        return jsonify({"message": "Document file uploaded", "filename": file.filename, "file_url": public_url}), 200
    else:
        return jsonify({"error": "File is not a supported document type", "file_type": file_type}), 400


@login_required
def audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file.content_type in ALLOWED_AUDIO_TYPES:
        destination_blob_name = f"audio/speeches/{file.filename}"
        public_url = upload_file_to_gcs(file, destination_blob_name)
        return jsonify({"message": "Audio file uploaded", "path": destination_blob_name, "file_url": public_url}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400


@login_required
def video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file.content_type in ALLOWED_VIDEO_TYPES:
        destination_blob_name = f"media/videos/{file.filename}"
        public_url = upload_file_to_gcs(file, destination_blob_name)
        return jsonify({"message": "Video file uploaded", "path": destination_blob_name, "file_url": public_url}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400


@login_required
def audio_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file.content_type in ALLOWED_TEXT_TYPES:
        destination_blob_name = f"audio/texts/{file.filename}"
        public_url = upload_file_to_gcs(file, destination_blob_name)
        return jsonify({"message": "Text file uploaded", "path": destination_blob_name, "file_url": public_url}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400


def search():
    print()


if __name__ == '__main__':
    app.run(debug=True)
