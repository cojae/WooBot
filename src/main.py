import picamera
import picamera.array
from time import sleep

import io
import cv2
import numpy

#Test camera functionality
with picamera.PiCamera() as camera :
    camera.resolution = (640,480)
    camera.vflip = False
    camera.hflip = False
    camera.brightness = 60
    with picamera.array.PiRGBArray(camera) as rawCapture :
        sleep(1.0) #Camera WarmUp
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array

        # Display the image on screen and wait for a keypress
        cv2.imshow("Image", image)
        cv2.waitKey(0)


print("Hello World")
