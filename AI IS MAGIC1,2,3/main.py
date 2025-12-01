import cv2
import numpy as np

# Load the pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open a video file
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Could not open video file.")
else:
    print("Video file opened successfully.")

# Counter for naming captured images
image_counter = 0

# Variable to store the previous face image
prev_face_img = None

# Threshold for face difference
difference_threshold = 3000

# Function to resize an image to a specific size
def resize_image(image, size=(227, 227)):
    return cv2.resize(image, size)

# Loop through each frame in the video
while True:
    # Read the next frame
    ret, frame = video_capture.read()

    # Break the loop if we have reached the end of the video
    if not ret:
        break

    # Convert the frame to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Crop and resize the current face
        current_face_img = resize_image(frame[y:y+h, x:x+w])

        # Check if the previous face is available
        if prev_face_img is not None:
            # Resize the previous face to match the current size
            prev_face_img_resized = resize_image(prev_face_img, size=current_face_img.shape[:2])

            # Calculate absolute difference between current and previous face images
            diff = np.sum(np.abs(current_face_img - prev_face_img_resized))

            # Check if the difference is above the threshold
            if diff > difference_threshold:
                # Save the frame when a face is significantly different from the last one
                cv2.imwrite(f'face_{image_counter}.png', current_face_img)
                image_counter += 1

        # Update previous face image
        prev_face_img = current_face_img

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
video_capture.release()
cv2.destroyAllWindows()
