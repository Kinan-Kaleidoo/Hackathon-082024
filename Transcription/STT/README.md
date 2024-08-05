# Speech-to-Text Transcription Service

This is a Flask-based service that performs speech-to-text transcription on audio extracted from video files. It uses the Whisper model from the `faster_whisper` library to transcribe audio and provide word-level timestamps.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Docker](#docker)
- [Requirements](#requirements)
- [License](#license)

## Installation

### Local Setup

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure `ffmpeg` is installed on your system. You can install it using your package manager, e.g., `apt-get` for Debian-based systems:

    ```bash
    sudo apt-get install ffmpeg
    ```

4. Run the Flask application:

    ```bash
    python app.py
    ```

   The application will start on `http://0.0.0.0:6060`.

### Docker Setup

1. Build the Docker image:

    ```bash
    docker build -t speech-to-text-service .
    ```

2. Run the Docker container:

    ```bash
    docker run -p 5000:5000 speech-to-text-service
    ```

   The application will be available at `http://localhost:5000`.

## Usage

### Endpoints

#### `/ms/stt` (POST)

**Description:** Transcribes audio extracted from a video file.

**Request:**

- **Content-Type:** `multipart/form-data`
- **Body:** A file field named `file` containing the video file to be transcribed. Supported formats include `mp3`, `wav`, `avi`, `mov`, `mp4`, `opus`, and `ogg`.

**Response:**

- **Content-Type:** `application/json; charset=utf-8`
- **Body:** A JSON object containing the transcription text and word-level timestamps.

    ```json
    {
      "text": "Transcribed text from audio",
      "timestamps": [
        [start_time_1, end_time_1],
        [start_time_2, end_time_2],
        ...
      ]
    }
    ```

**Example Request:**

```bash
curl -X POST -F "file=@/path/to/video.mp4" http://localhost:5000/ms/stt
