# Flask Text-to-Speech API

This is a Flask-based API that converts text from an uploaded file to speech using Google Cloud Text-to-Speech. The API accepts a text file, synthesizes speech from the text (limited to the first 30 words), and returns an audio file.

## Features

- Accepts text file uploads
- Converts text to speech using Google Cloud Text-to-Speech
- Limits speech synthesis to the first 30 words of the text
- Returns the synthesized speech as an audio file

## Prerequisites

- Docker
- Google Cloud Project with Text-to-Speech API enabled
- Python 3.12

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/flask-text-to-speech.git
   cd flask-text-to-speech
