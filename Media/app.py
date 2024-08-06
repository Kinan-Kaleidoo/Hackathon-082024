from flask import Flask, jsonify, request
from google.cloud import storage
from PIL import Image
import io
from io import BytesIO
import moviepy.editor as mp
import multiprocessing
from dotenv import load_dotenv
import os
#import Face_recognition.face_recognition_script as fr
#import Description.description as d
from Object_Detection.Object_detection import obj_detection_image
from meta.get_meta_image import extract_image_info
from Face_recognition.face_recognition_script import recogtion
from Face_detection.face_detection import face_detection_image_dlib
from Description.description import description
from google.oauth2 import service_account
import requests


load_dotenv()
app = Flask(__name__)


# Path to your service account key file
key_path = 'hackathon-082024-38c5136c029f.json'

# Create credentials object
credentials = service_account.Credentials.from_service_account_file(key_path)

# Create a client with the specified credentials
client = storage.Client(credentials=credentials)

# Access the bucket name from an environment variable
bucket_name = os.getenv('BUCKET_NAME')
print(f'Bucket name: {bucket_name}')
# Retrieve the bucket
bucket = client.get_bucket(bucket_name)


def worker(func, param, queue, index):
    result = func(param)
    queue.put((index, result))


def faces(image):
    faces = face_detection_image_dlib(image)
    ids = [recogtion(Image.open(f'/Face_detection/{face_url}')) for face_url in faces]
    return [(face,ids[i]) for i,face in enumerate(faces)]

@app.route('/image', methods=['POST'])
def process_image():
 

    queue = multiprocessing.Queue()

    # Retrieve the URL from query parameters
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400


    # Fetch the image
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    image_data = BytesIO(response.content)

    # Open the image with Pillow
    image = Image.open(image_data)
    #'faces': [(face_url,recogtion(Image.open(face_url))) for face_url in ___],
    # Prepare a response (e.g., image dimensions or some metadata)
   
    pram = [image, url, image, url]
    functions = [extract_image_info,description,faces,obj_detection_image]

    for index in range(len(functions)):
        p = multiprocessing.Process(target=worker, args=(functions[index], pram[index], queue, index))
        p.start()
        
    for index in range(len(functions)):
        p.join()

    results = [queue.get() for _ in range(len(functions))]
    results.sort(key=lambda x: x[0])    
    response_data = {
        'meta': results[0][1],
        'description': results[1][1],
        'faces': results[2][1],
        'tags': results[3][1][1]
    }   

    # Sort results based on index
    results.sort(key=lambda x: x[0])

    

    return jsonify(response_data)

  

@app.route('/video/<url>', methods=['POST'])
def greet2(url):
    response = {
    }
    blob = bucket.blob(url)
        # Download the video data as bytes
    video_data = blob.download_as_bytes()

    # Open the video using moviepy
    video_clip = mp.VideoFileClip(io.BytesIO(video_data))













    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)