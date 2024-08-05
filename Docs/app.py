import os
import json
import requests
from flask import Flask, request, jsonify
from google.cloud import documentai_v1 as documentai
from google.cloud import storage

app = Flask(__name__)

# Set the environment variable for Google Cloud authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Hakathon_key.json"

# Function to download a file from a URL
def download_file_from_url(url, local_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"Failed to download file from URL: {url}")

# Function to process a document using Google Document AI
def process_document_sample(project_id, location, processor_id, file_path, mime_type):
    client_options = {"api_endpoint": "eu-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # Read the document content
    with open(file_path, "rb") as file:
        document_content = file.read()

    # Configure the request
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=document_content, mime_type=mime_type)
    )

    # Process the document
    result = client.process_document(request=request)
    document = result.document

    # Extract text and entities
    text = document.text
    entities = extract_entities(document)

    return text, entities

# Function to extract entities from the document
def extract_entities(document):
    entities = []
    for entity in document.entities:
        entities.append({
            "type": entity.type_,
            "mention_text": entity.mention_text,
            "confidence": entity.confidence
        })
    return entities

# Function to convert the extracted data to JSON
def convert_to_json(file_path, google_text, entities):
    data = {
        "file_name": os.path.basename(file_path),
        "google_text": google_text,
        "entities": entities
    }
    return json.dumps(data, indent=4, ensure_ascii=False)

@app.route('/ms/doc', methods=['POST'])
def process_document():
    data = request.json
    if 'file_url' not in data:
        return jsonify({"error": "No file URL provided"}), 400

    file_url = data['file_url']
    file_name = file_url.split("/")[-1]
    file_path = f"/tmp/{file_name}"

    try:
        # Download the file from the provided URL
        download_file_from_url(file_url, file_path)

        project_id = "151720227861"  # Your project ID
        location = "eu"  # Your processor location
        processor_id = "ebabe2c425bfb7c4"  # Your processor ID
        mime_type = "application/pdf"  # MIME type of your document

        # Extract entities with Google Document AI
        google_text, entities = process_document_sample(project_id, location, processor_id, file_path, mime_type)
        # Convert to JSON
        json_output = convert_to_json(file_path, google_text, entities)

        response = jsonify(json.loads(json_output))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
