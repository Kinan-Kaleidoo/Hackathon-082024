import os
import magic
import requests
from google.cloud import storage
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_login import login_required
from db import get_document_by_url, insert_document, update_document, update_media_document
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
        public_url = upload_file_to_gcs(file, destination_blob_name)
        external_api_base_url = 'http://media-service:8086/ms/media'
        external_api_url = f"{external_api_base_url}?url={public_url}"
        requests.post(external_api_url)
        return jsonify(
            {"message": "File uploaded successfully", "path": destination_blob_name, "file_url": public_url}), 200
    elif file_type in ALLOWED_VIDEO_TYPES:
        destination_blob_name = f"media/videos/{file.filename}"
        public_url = upload_file_to_gcs(file, destination_blob_name)
        external_api_base_url = 'http://media-service:8086/ms/media'
        external_api_url = f"{external_api_base_url}?url={public_url}"
        requests.post(external_api_url)
        return jsonify(
            {"message": "File uploaded successfully", "path": destination_blob_name, "file_url": public_url}), 200
    else:
        return jsonify({"error": "File is not an image or video", "file_type": file_type}), 400


def media_result():
    data = request.get_json()
    result = data.get('result')
    url = data.get('url')
    if not result:
        return jsonify({'error': 'Text is required'}), 400
    update_media_document(url, result)
    external_api_url = 'frontend-service:8081/media_result'
    requests.post(external_api_url, json={'result': result})


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



def allowed_file_audio(content_type):
    allowed_mime_types = {'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/mp4'}
    return content_type in allowed_mime_types


def inner_nlp(url):
    response = requests.post('/ms/nlp', json={"url": url})


def nlp_improve():
    response = requests.post('/ms/nlp/improve')


def nlp_subject_extract():
    response = requests.post('/ms/nlp/subject_extract')


def nlp_summary_text():
    response = requests.post('/ms/nlp/summary_text')


def nlp_sentiment_analysis():
    response = requests.post('/ms/nlp/sentiment_analysis')

@login_required

def nlp():
    if request.is_json:
        data = request.get_json()
        url = data.get('url')

        if url:
            existing_document = get_document_by_url(url)
            if existing_document:
                # Update the existing document with the new data
                update_document(url, data)
                return jsonify({"message": "Document updated successfully!"}), 200

        else:
            return jsonify({"error": "URL is required"}), 400

    else:
        return jsonify({"error": "Request body must be JSON"}), 400


"""
Bashar:

    app.add_url_rule('/improve', 'improve', improve,methods=["POST", "GET"])
    app.add_url_rule('/subject_extract', 'subject_extract', subject_extract,methods=["POST", "GET"])
    app.add_url_rule('/summary_text', 'summary_text', summary_text,methods=["POST", "GET"])
    app.add_url_rule('/sentiment_analysis', 'sentiment_analysis', sentiment_analysis,methods=["POST", "GET"])
"""


def ms_media():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        return jsonify({"success": True, "message": "File uploaded successfully", "file": file}), 200


def ms_audio():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        return jsonify({"success": True, "message": "File uploaded successfully", "file": file}), 200


def ms_search():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        return jsonify({"success": True, "message": "File uploaded successfully", "file": file}), 200


def ms_doc():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            # TODO URL
        url = f"gs://{bucket_name}/docs/{file.filename}"
        return jsonify({"success": True, "message": "File uploaded successfully", "url": url}), 200


def nlp_improve():
    data = request.get_json()
    text = data.get('text')
    url = data.get('url')
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    update_document(url, text)
    external_api_url = 'frontend-service:8081/nlp_improve'
    requests.post(external_api_url, json={'text': text})


def nlp_subject_extract():
    data = request.get_json()
    subject = data.get('subject')
    url = data.get('url')
    if not subject:
        return jsonify({'error': 'Text is required'}), 400
    update_document(url, subject)
    external_api_url = 'frontend-service:8081/nlp_subject_extract'
    requests.post(external_api_url, json={'subject': subject})


def nlp_summary_text():
    data = request.get_json()
    summary = data.get('summary')
    url = data.get('url')
    if not summary:
        return jsonify({'error': 'Text is required'}), 400
    update_document(url, summary)
    external_api_url = 'frontend-service:8081/nlp_summary_text'
    requests.post(external_api_url, json={'summary': summary})


def nlp_sentiment_analysis():
    data = request.get_json()
    sentiment = data.get('sentiment')
    url = data.get('url')
    if not sentiment:
        return jsonify({'error': 'Text is required'}), 400
    update_document(url, sentiment)
    external_api_url = 'frontend-service:8081/nlp_sentiment_analysis'
    requests.post(external_api_url, json={'sentiment': sentiment})


if __name__ == '__main__':
    app.run(debug=True)
