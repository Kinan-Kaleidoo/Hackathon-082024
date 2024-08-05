import os
from flask import Flask, request, send_file
from google.cloud import texttospeech
import tempfile

app = Flask(__name__)

def truncate_text(text, word_limit=30):
    words = text.split()
    return ' '.join(words[:word_limit])

@app.route('/synthesize', methods=['POST'])
def synthesize_speech():
    if 'text_file' not in request.files:
        return "No file part", 400

    file = request.files['text_file']
    if file.filename == '':
        return "No selected file", 400

    text = file.read().decode('utf-8')
    truncated_text = truncate_text(text)

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=truncated_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="he-IL",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
        temp_audio_file.write(response.audio_content)
        temp_audio_file_path = temp_audio_file.name

    return send_file(temp_audio_file_path, as_attachment=True, download_name='output.mp3')

if __name__ == '__main__':
    app.run(debug=True)
