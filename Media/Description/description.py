from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from transformers import BartTokenizer, BartForConditionalGeneration
from PIL import Image
import requests
import cv2
import os
from io import BytesIO
import mimetypes

# Load the summarization model and tokenizer
summarization_model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
summarization_tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

# Load the pre-trained model and tokenizer
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

def summarize_captions(captions, max_length=150):
    # Concatenate captions into a single text
    text = " ".join(captions)

    # Encode the text and generate summary
    inputs = summarization_tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = summarization_model.generate(inputs, max_length=max_length, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    
    summary = summarization_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def generate_caption(image):
    # Preprocess the image
    inputs = image_processor(images=image, return_tensors="pt")
    pixel_values = inputs.pixel_values

    # Generate the caption
    output_ids = model.generate(pixel_values, max_length=50, num_beams=4, early_stopping=True)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return caption

def process_image(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    caption = generate_caption(image)
    return caption

def extract_key_frames(video_path, interval=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % interval == 0:  # Select key frames at specified intervals
            frames.append(frame)
        frame_count += 1
    cap.release()
    return frames

def cleanup_frames(output_folder):
    for file_name in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

def process_video(video_url, output_folder='Media/Description/frames'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Download the video
    response = requests.get(video_url)
    video_path = os.path.join(output_folder, 'video.mp4')
    with open(video_path, 'wb') as f:
        f.write(response.content)

    # Extract key frames from video
    frames = extract_key_frames(video_path, interval=30)
    captions = []

    for idx, frame in enumerate(frames):
        frame_file = os.path.join(output_folder, f"frame_{idx:04d}.jpg")
        cv2.imwrite(frame_file, frame)
        
        # Load and preprocess the image
        image = Image.open(frame_file).convert("RGB")
        caption = generate_caption(image)
        captions.append(caption)

    # Summarize captions
    video_caption = summarize_captions(captions)

    # Cleanup frame files
    cleanup_frames(output_folder)

    return video_caption


def process_url(url):
    # Determine the content type
    mime_type, _ = mimetypes.guess_type(url)
    
    if mime_type:
        if mime_type.startswith('image'):
            return process_image(url)
        elif mime_type.startswith('video'):
            return process_video(url)
    else:
        # Check the file extension if mime type is not available
        if url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            return process_image(url)
        elif url.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            return process_video(url)
    
    return "Unsupported file type"

def description(url):
    return process_url(url)

# # Example usage
# urls = [
#     'https://videos.pexels.com/video-files/2308576/2308576-sd_640_360_30fps.mp4',
#     'https://h5p.org/sites/default/files/h5p/content/1209180/images/file-6113d5f8845dc.jpeg'
# ]

# for url in urls:
#     caption = description(url)
#     print("--------------------------------")
#     if caption:
#         print(f"Caption for {url}: {caption}")
#     else:
#         print("No caption!")
