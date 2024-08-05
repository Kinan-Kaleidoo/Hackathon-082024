from flask import Flask, request, jsonify
from flask_login import login_required


def login():
    return None


@login_required
def index():
    return None

@login_required
def media():
    return None

@login_required
def search():
    return None

@login_required
def doc():
    return None

# @login_required
def audio():
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

@login_required
def video():
    return None
