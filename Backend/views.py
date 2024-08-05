import os
import magic
import requests
from google.cloud import storage
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_login import login_required
from db import get_document_by_url, insert_document, update_document



load_dotenv()

# Initialize Google Cloud Storage client
storage_client = storage.Client()
bucket_name = os.getenv('GOOGLE_CLOUD_BUCKET_NAME')
if not bucket_name:
    raise ValueError("Environment variable GOOGLE_CLOUD_BUCKET_NAME not set.")
bucket = storage_client.bucket(bucket_name)


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
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file:
            file_content = file.read()
            mime = magic.Magic(mime=True)
            file_type = mime.from_buffer(file_content)
            if file_type in ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                return jsonify({"filename": file.filename, "format": file_type}), 200
            else:
                return jsonify({"error": "File is not a PDF, TXT, or WORD document", "file_type": file_type}), 400
        return jsonify({"error": "No file provided"}), 400
    else:
        return jsonify("good"), 200
      

# @login_required
def audio():
    print()


@login_required
def video():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file and allowed_file_audio(file.content_type):
            # Process the audio file here
            return jsonify({"message": "Audio file received"}), 200
        else:
            return jsonify({"error": "Invalid file type"}), 400
    return "Please upload an audio file", 200


def audio_text():
    if request.method == 'POST':
        # Try to get text from JSON payload
        if request.is_json:
            data = request.get_json()
            text = data.get('text', '')
        else:
            # Try to get text from form data
            text = request.form.get('text', '')

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Optionally, validate the text (e.g., language, inappropriate content)
        # Here, you can include any additional checks you need

        # At this point, you have valid text to convert to audio
        return jsonify({"message": "Text received", "text": text}), 200

    elif request.method == 'GET':
        # Handle GET requests if necessary
        return "Please send a POST request with text data to convert to audio.", 200


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
