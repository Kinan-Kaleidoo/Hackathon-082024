import cv2
from typing import Tuple, List
from ultralytics import YOLO
import numpy as np
import requests
from io import BytesIO
from PIL import Image

def obj_detection_image(image_path: str) -> Tuple[str, List[str]]:
    """
    Perform object detection on an image and return the path of the annotated image and detected objects with high confidence.
    
    Args:
        image_path (str): Path or URL to the image file.
    
    Returns:
        Tuple[str, List[str]]: The path of the annotated image and a list of detected objects.
    """
    # Check if image_path is a URL or a local file path
    if image_path.startswith('http://') or image_path.startswith('https://'):
        # Download the image from the URL
        response = requests.get(image_path)
        image = Image.open(BytesIO(response.content))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    else:
        # Load the image from a local file path
        image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError(f"Error loading image: {image_path}")
    # Initialize YOLO model
    model = YOLO('yolov8n.pt')

    # Perform inference on the image
    results = model(np.array(image))

    # Check the type of results
    if isinstance(results, list):
        result = results[0]  # Assuming the first item is what you need
    else:
        result = results

    # Access detailed results
    detected_objects = []
    if hasattr(result, 'boxes'):
        # Extract data
        boxes = result.boxes.xyxy.cpu().numpy() if hasattr(result.boxes, 'xyxy') else []
        scores = result.boxes.conf.cpu().numpy() if hasattr(result.boxes, 'conf') else []
        labels = result.names if hasattr(result, 'names') else []

        # Draw bounding boxes and labels on the image
        for (x1, y1, x2, y2), score, label in zip(boxes, scores, result.boxes.cls.cpu().numpy()):
            if score > 0.5:
                label_name = labels[int(label)]

                # Draw bounding box
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                
                # Put label text
                cv2.putText(image, f'{label_name} {score:.2f}', (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Append detected object to the list
                detected_objects.append(label_name)
    else:
        print("No bounding boxes found. Check the result structure.")
    
    # Save the annotated image locally
    annotated_image_path = 'annotated_image.jpg'
    cv2.imwrite(annotated_image_path, image)

    return annotated_image_path, detected_objects


def obj_detection_video(video_url: str) -> Tuple[str, List[str]]:
    """
    Perform object detection on a video and return the path of the annotated video and detected objects with high confidence.
    
    Args:
        video_url (str): Path or URL to the video file.
    
    Returns:
        Tuple[str, List[str]]: The local path of the annotated video and a list of detected objects for each frame.
    """
    # Load the video
    video = cv2.VideoCapture(video_url)
    if not video.isOpened():
        raise ValueError(f"Error opening video: {video_url}")
    
    # Initialize YOLO model
    model = YOLO('yolov8n.pt')
    
    # Get video properties
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    
    # Define codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use other codecs if needed
    annotated_video_path = 'annotated_video.mp4'
    out = cv2.VideoWriter(annotated_video_path, fourcc, fps, (frame_width, frame_height))
    
    all_detected_objects = []

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        
        # Perform inference on the frame
        results = model(frame)

        # Check the type of results
        if isinstance(results, list):
            result = results[0]  # Assuming the first item is what you need
        else:
            result = results

        # Access detailed results
        detected_objects = set()
        if hasattr(result, 'boxes'):
            # Extract data
            boxes = result.boxes.xyxy.cpu().numpy() if hasattr(result.boxes, 'xyxy') else []
            scores = result.boxes.conf.cpu().numpy() if hasattr(result.boxes, 'conf') else []
            labels = result.names if hasattr(result, 'names') else []

            # Draw bounding boxes and labels on the frame
            for (x1, y1, x2, y2), score, label in zip(boxes, scores, result.boxes.cls.cpu().numpy()):
                if score > 0.7:  # Filter by score > 70%
                    label_name = labels[int(label)]

                    # Draw bounding box
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    
                    # Put label text
                    cv2.putText(frame, f'{label_name} {score:.2f}', (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    # Append detected object to the list
                    detected_objects.add(label_name)
        
        # Append detected objects of the current frame to the overall list
        all_detected_objects.extend(detected_objects)
        
        # Write the annotated frame to the output video
        out.write(frame)
    
    # Release video objects
    video.release()
    out.release()
    
    return all_detected_objects #annotated_video_path, 