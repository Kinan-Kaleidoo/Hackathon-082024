import json

def create_default_file(json_path):
    """Create a default empty JSON file."""
    default_data = {}
    with open(json_path, 'w') as file:
        json.dump(default_data, file)

# Path to your JSON file
json_path = 'Face_recognition/face_data.json'

# Create the default file
create_default_file(json_path)
