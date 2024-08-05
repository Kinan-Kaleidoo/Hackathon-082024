import os
import json
from flask import Flask, request, jsonify
from google.cloud import documentai_v1 as documentai
from google.cloud import storage
from io import BytesIO

app = Flask(__name__)

# Set the environment variable for Google Cloud authentication
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Docs/Hakathon_key.json"

# Function to download a file from Google Cloud Storage
def download_blob(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    file_content = blob.download_as_bytes()
    return file_content

# Function to process a document using Google Document AI
def process_document_sample(project_id, location, processor_id, file_content, mime_type):
    client_options = {"api_endpoint": "eu-documentai.googleapis.com"}
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # Configure the request
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=file_content, mime_type=mime_type)
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
def convert_to_json(file_name, google_text, entities):
    data = {
        "file_name": file_name,
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
    bucket_name, blob_name = parse_gcs_url(file_url)

    try:
        # Download the file from Google Cloud Storage
        file_content = download_blob(bucket_name, blob_name)
        file_name = os.path.basename(blob_name)
        mime_type = "application/pdf"  # Update MIME type if needed

        project_id = "151720227861"  # Your project ID
        location = "eu"  # Your processor location
        processor_id = "ebabe2c425bfb7c4"  # Your processor ID

        # Extract entities with Google Document AI
        google_text, entities = process_document_sample(project_id, location, processor_id, file_content, mime_type)
        # Convert to JSON
        json_output = convert_to_json(file_name, google_text, entities)

        response = jsonify(json.loads(json_output))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def parse_gcs_url(url):
    """Parse a GCS URL into bucket name and blob name."""
    if not url.startswith("gs://"):
        raise ValueError("Invalid URL format. Must start with gs://")
    path = url[len("gs://"):]
    bucket_name, blob_name = path.split("/", 1)
    return bucket_name, blob_name

if __name__ == '__main__':
    app.run(debug=True)
