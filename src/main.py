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

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
            break

print("Hello World")
