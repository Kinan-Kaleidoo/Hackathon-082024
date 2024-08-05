import dlib
import cv2
import numpy as np
from typing import List

def face_detection_image_dlib(img_url: str):
    """
    Perform face detection on an image using Dlib and return the annotated image, detected face coordinates,
    and saved face images.
    
    Args:
        img_url (str): Path or URL to the image file.
    
    Returns:
        Tuple[np.ndarray, List[Tuple[int, int, int, int]], List[str]]: The annotated image, a list of tuples
        with detected face coordinates, and a list of file paths where each face image is saved.
    """
    # Load the image
    image = cv2.imread(img_url)
    if image is None:
        raise ValueError(f"Error loading image: {img_url}")

    # Initialize Dlib's face detector
    detector = dlib.get_frontal_face_detector()

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = detector(gray)

    # Draw bounding boxes around detected faces
    face_rects = []
    face_images = []
   
    for i, face in enumerate(faces):
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        face_rects.append((x, y, w, h))
        
        # Crop the face from the image
        face_image = image[y:y+h, x:x+w]
        
        # Save the face image
        face_filename = f"face_{i}.jpg"
        cv2.imwrite(face_filename, face_image)
        face_images.append(face_filename)
        
    return face_images # upload to gcp bucket in the main



def face_detection_video_dlib(video_url: str, sample_interval: int = 10) -> List[str]:
    """
    Perform face detection on a video using Dlib, sample frames, and return saved face images with consistent filenames.
    
    Args:
        video_url (str): Path or URL to the video file.
        sample_interval (int): Number of frames to skip between samples.
    
    Returns:
        List[str]: A list of file paths where each face image is saved.
    """
    # Load the video
    video = cv2.VideoCapture(video_url)
    if not video.isOpened():
        raise ValueError(f"Error opening video: {video_url}")

    # Initialize Dlib's face detector
    detector = dlib.get_frontal_face_detector()

    # Initialize face tracker
    tracker = dlib.correlation_tracker()

    face_images = []
    frame_count = 0
    sampled_frame_count = 0
    trackers = []  # List to hold active trackers

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        
        if frame_count % sample_interval == 0:
            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Perform face detection
            faces = detector(gray)

            # Update trackers
            for tracker in trackers:
                tracker.update(frame)
                pos = tracker.get_position()
                x, y, w, h = int(pos.left()), int(pos.top()), int(pos.width()), int(pos.height())
                face_image = frame[y:y+h, x:x+w]
                face_filename = f"face_frame_{sampled_frame_count}_tracked.jpg"
                cv2.imwrite(face_filename, face_image)
                face_images.append(face_filename)

            # Add new trackers for newly detected faces
            for face in faces:
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                new_tracker = dlib.correlation_tracker()
                new_tracker.start_track(frame, dlib.rectangle(x, y, x+w, y+h))
                trackers.append(new_tracker)

            sampled_frame_count += 1
        
        frame_count += 1

    # Release the video object
    video.release()

    return face_images
