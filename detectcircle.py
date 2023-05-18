import cv2
import numpy as np
from statistics import mode,mean
#import senddata

list_max_size=10
x_coords= [0]*list_max_size#list of 10 zeros
y_coords= [0]*list_max_size

cap = cv2.VideoCapture("C:/Users/Ahmed/Desktop/micro2/project/aimm/try2/g.mp4")#0 for camera#"C:/Users/Ahmed/Desktop/micro2/project/aimm/v.mp4" for video
thank_you = 0
while True:
    # Capture frame-by-frame
    success, frame = cap.read()

    if not success:
        print("Cannot read the video file")
        break
    if(thank_you == 0):
        height, width, _ = frame.shape
        print("Frame size: {}x{}".format(width, height))
        thank_you = 1

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper range of the red color
    lower_green = np.array([45, 100, 20])
    upper_green = np.array([90, 255, 255])

    #lower_red2 = np.array([170, 50, 50])
    #upper_red2 = np.array([180, 255, 255])

    # Create a mask to extract only the red pixels
    #mask1 = cv2.inRange(hsv, lower_red, upper_red)
    #mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    #mask = cv2.bitwise_or(mask1, mask2)
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Apply a blur to the mask to reduce noise
    blur = cv2.GaussianBlur(mask, (5, 5), 0)

    # Detect circles using the Hough transform
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1, minDist=30, param1=50, param2=20, minRadius=0, maxRadius=0)#min max 0 0 for no conditions

    # Draw the detected circles on the original image
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x_img, y_img, r) in circles:

            x=x_img-(width /2)#to covert it from [0:640] to [-320:320]
            y=y_img-(height/2)

            if len(x_coords) > 10:
                x_coords.pop(0)
                y_coords.pop(0)

            x_coords.append(x)
            y_coords.append(y)

            x_repeated=mode(x_coords)
            y_repeated=mode(y_coords)

            #x_repeated=mean(x_coords)
            #y_repeated=mean(y_coords)

            x_repeated_img=int(x_repeated+(width /2))
            y_repeated_img=int(y_repeated+(height /2))

            #print("x_repeated,y_repeated",x_repeated_img,y_repeated,x,y,"list",x_coords)
            #cv2.circle(frame, (x_repeated_img, y_repeated_img), r+2, (255, 0, 0), 2)
            cv2.circle(frame, (x_img, y_img), r, (0, 255, 255), 3)

            print("Circle center: ({}, {}),R:".format(x, y),r)

            #send x and y to esp32
            x_str=str(x_repeated)
            y_str=str(y_repeated)
            #senddata.send_data(x_str)
            #senddata.send_data(y_str)

    # Display the result
    cv2.imshow('Result', frame)
    #cv2.waitKey(500)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()