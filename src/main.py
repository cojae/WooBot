import picamera
from time import sleep

#Test camera functionality
camera = picamera.PiCamera()
camera.vflip = False
camera.hflip = False
camera.brightness = 60

camera.start_preview()
sleep(1.0)
camera.stop_preview()


print("Hello World")
