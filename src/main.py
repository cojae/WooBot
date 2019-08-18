import picamera
from time import sleep

import io
import cv2
import numpy

#Test camera functionality
camera = picamera.PiCamera()
camera.vflip = False
camera.hflip = False
camera.brightness = 60

camera.start_preview()
sleep(10.0)
camera.stop_preview()


print("Hello World")
