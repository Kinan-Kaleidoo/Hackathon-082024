from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib.pyplot as plt

def obj_detection_image(img_url):
    """
    Perform object detection on an image and return the annotated image and detected objects with high confidence.
    
    Args:
        img_url (str): Path or URL to the image file.
    
    Returns:
        Tuple[np.ndarray, List[Dict[str, Any]]]: The annotated image and a list of dictionaries with detected objects.
    """
    # Load the image
    image = cv2.imread(img_url)
    if image is None:
        raise ValueError(f"Error loading image: {img_url}")

    # Initialize YOLO model
    model = YOLO('yolov8n.pt')

    # Perform inference on the image
    results = model(image)

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
    
    # Convert image from BGR to RGB format for consistency
    annotated_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    return annotated_image, detected_objects  # Returning annotated image and list of object labels

# # Example usage
# img_url = 'dog_bycicle.jpg'
# annotated_image, detected_objects = obj_detection_image(img_url)
# print("Detected objects:", detected_objects)
# # Display the image using matplotlib
# plt.imshow(annotated_image)
# plt.axis('off')  # Turn off axis numbers and ticks
# plt.show()

def obj_detection_video(video_url):
    """
    Perform object detection on a video and return the annotated video and detected objects with high confidence.
    
    Args:
        video_url (str): Path or URL to the video file.
    
    Returns:
        List[str]: A list of labels of detected objects for each frame.
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
    out = cv2.VideoWriter('annotated_video.mp4', fourcc, fps, (frame_width, frame_height))
    
    frame_count = 0
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
        
        # Increment frame count
        frame_count += 1
    
    # Release video objects
    video.release()
    out.release()
    
    return 'annotated_video.mp4', all_detected_objects

# # Example usage
# video_url = 'one-by-one-person-detection.mp4'
# annotated_video_path, detected_objects = obj_detection_video(video_url)

# print(f"Annotated video saved at: {annotated_video_path}")
# print("Detected objects:", detected_objects)

# # To display the annotated video frame by frame using matplotlib
# annotated_video = cv2.VideoCapture(annotated_video_path)

# while annotated_video.isOpened():
#     ret, frame = annotated_video.read()
#     if not ret:
#         break