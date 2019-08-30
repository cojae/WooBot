import picamera
import picamera.array
from time import sleep

import io
import cv2
import numpy

# Initialize the camera and camera capture
camera = picamera.PiCamera()
rawCapture = picamera.array.PiRGBArray(camera, size=(640,480))

camera.resolution = (640,480)
camera.vflip = False
camera.hflip = False
camera.framerate = 32
camera.brightness = 60

# Camera WarmUp
sleep(1.0)

# Pulled from opencv default data
face = cv2.CascadeClassifier('./dataset/haarcascade_frontalface_default.xml')

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    grayImage = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )

    # use dataset training to determine if a face is present
    faces = face.detectMultiScale(image, 1.3, 5)

    # Put rectangle in every face it picks up
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = grayImage[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]
    
    cv2.imshow('Stream',image)

    key = cv2.waitKey(1) & 0xFF

    # Clear the captured frame
    rawCapture.truncate(0)

    if key == ord("q"):
        cv2.destroyAllWindows()
        break

print("Exiting")
camera.close()
