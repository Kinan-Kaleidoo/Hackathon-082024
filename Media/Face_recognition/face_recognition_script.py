import json
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-trained ResNet model
model = models.resnet50(pretrained=True)
model.eval()

def extract_features(img):
    """Extract features from an image using ResNet."""
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    
    img_tensor = preprocess(img).unsqueeze(0)

    with torch.no_grad():
        features = model(img_tensor)
    return features.numpy().flatten()

def load_face_data(json_path):
    """Load face ID and vectors from a JSON file."""
    try:
        with open(json_path, 'r') as file:
            face_data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"Error: The file {json_path} is not valid or does not exist. Initializing empty data.")
        face_data = {}
    return face_data

def save_face_data(json_path, face_data):
    """Save face ID and vectors to a JSON file."""
    with open(json_path, 'r+') as file:
        try:
            existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}
        
        # Update existing data with new face data
        existing_data.update(face_data)
        
        # Move cursor to the beginning of the file
        file.seek(0)
        # Write the updated data back to the file
        json.dump(existing_data, file)
        # Truncate any remaining part of the file (in case the new data is shorter)
        file.truncate()

def find_face_id(face_vector, face_data, threshold=0.8):
    """Find face ID based on feature vector similarity."""
    face_vector = np.array(face_vector).reshape(1, -1)  # Reshape for cosine similarity
    for face_id, vector in face_data.items():
        vector = np.array(vector).reshape(1, -1)  # Reshape for cosine similarity
        similarity = cosine_similarity(face_vector, vector)[0][0]
        if similarity > threshold:
            return face_id
    return None

def get_next_id(face_data):
    """Generate the next integer ID."""
    if face_data:
        max_id = max(int(face_id) for face_id in face_data.keys())
        return str(max_id + 1)
    return '1'

def add_face_id(face_id, face_vector, face_data):
    """Add new face ID and vector to the data."""
    face_data[face_id] = face_vector

def recogtion(img):
    # Example usage
    json_path = 'Face_recognition/face_data.json'
    face_data = load_face_data(json_path)

    # Extract features from a new image
  
    new_face_vector = extract_features(img)

    # Generate a new unique ID
    new_face_id = get_next_id(face_data)



    # Find if the face ID already exists
    existing_face_id = find_face_id(new_face_vector, face_data)

    if existing_face_id:
        print(f"Face ID found: {existing_face_id}")
        return existing_face_id
    else:
        print("New face ID will be added.")
        add_face_id(new_face_id, new_face_vector.tolist(), face_data)  # Convert to list for JSON serialization
        save_face_data(json_path, {new_face_id: new_face_vector.tolist()})
        print(f"New face ID {new_face_id} added.")
    
    return new_face_id
