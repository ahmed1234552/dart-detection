import cv2
import time
import numpy as np

# # Define the lower and upper bounds for green color in HSV
lower_green = np.array([45, 100, 100])
upper_green = np.array([75, 255, 255])

# Create a VideoCapture object to read from the webcam
cap = cv2.VideoCapture("C:/Users/Ahmed/Desktop/micro2/project/aimm/try2/g.mp4")#"C:/Users/Ahmed/Desktop/micro2/project/aimm/try2/aim2.mp4"

while True:
    # Read the current frame from the video stream
    success, frame = cap.read()
    #frame = cv2.resize(frame,(640,480))

    if not success:
        print("Unable to read frame")
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the frame to get only red pixels
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the binary image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    (x, y), radius = cv2.minEnclosingCircle(max(contours, key=cv2.contourArea))
    center = (int(x), int(y))
    radius = int(radius)

    # Draw a circle around the detected object
    cv2.circle(frame, center, radius, (0, 255, 255), 4)

    # Display the frame with the detected circle
    cv2.imshow('Video', frame)

    time.sleep(1/10)
    # Check for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()
