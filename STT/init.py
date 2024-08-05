import torch
from faster_whisper import WhisperModel


# Initialize the Whisper model
def load_model():
    if torch.cuda.is_available():
        model = WhisperModel("ivrit-ai/faster-whisper-v2-d3-e3")  # GPU case
    else:
        model = WhisperModel('base')  # CPU case
    return model