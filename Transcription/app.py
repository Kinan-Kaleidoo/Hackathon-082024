from flask import Flask, request, jsonify, Response
import os
from werkzeug.utils import secure_filename
import json
from init import load_model
from utils import allowed_file, extract_audio_from_video

app = Flask(__name__)

model = load_model()

@app.route('/ms/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    filename = secure_filename(file.filename)

    # Ensure the static directory exists
    if not os.path.exists("static"):
        os.makedirs("static")

    # Save the uploaded video file
    video_path = os.path.join("static", filename)
    file.save(video_path)

    # Extract audio from video
    audio_output_path = os.path.join("static", "output_audio.wav")
    extract_audio_from_video(video_path, audio_output_path)

    # Perform transcription with word timestamps
    result = model.transcribe(audio_output_path, language='he', word_timestamps=True)

    # Extract segments from the generator
    segments = list(result[0])  # Convert generator to a list

    # Extract word-level timestamps
    word_timestamps = []
    full_text = []
    for segment in segments:
        full_text.append(segment.text)
        for word_info in segment.words:
            word_timestamps.append(word_info.start)
            word_timestamps.append(word_info.end)

    response = {
        "text": " ".join(full_text).strip(),
        "timestamps": word_timestamps
    }

    response_json = json.dumps(response, ensure_ascii=False)
    return Response(response_json, content_type="application/json; charset=utf-8")

if __name__ == '__main__':
    app.run(debug=True)