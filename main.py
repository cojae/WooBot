import picamera
import picamera.array
import time 
import os
import random

import io
import cv2
import numpy

# This might be over-kill, but this library will do the audio playing
# Perhaps find one that isn't as expansive as this one
import pygame

def decideSound():
    retString = ""
    fileList = [os.path.join("./sounds/",f) for f in os.listdir("./sounds")]
    print(fileList)
    return fileList[random.randrange(0,len(fileList))]

def playSound(soundFile):
    pygame.mixer.music.load(soundFile)
    pygame.mixer.music.play()

# Initialize the camera and camera capture
camera = picamera.PiCamera()
rawCapture = picamera.array.PiRGBArray(camera, size=(640,480))

# Initialize pygame which will be used to play audio
pygame.init()

camera.resolution = (640,480)
camera.vflip = False
camera.hflip = False
camera.framerate = 32
camera.brightness = 60

# Camera WarmUp
time.sleep(1.0)

# Pulled from opencv default data
face = cv2.CascadeClassifier('./dataset/haarcascade_frontalface_default.xml')
profileFace = cv2.CascadeClassifier('./dataset/haarcascade_profileface.xml')

# To keep track of time when last audio was heard
lastTime = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    grayImage = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )

    # use dataset training to determine if a face is present
    faces = face.detectMultiScale(image, 1.3, 5)

    imageSeen = ( len(faces) != 0 )

    # If we don't find any faces, try profile face detection
    # I honestly don't know the difference and will need to look it up TODO
    if False == imageSeen:
        faces = profileFace.detectMultiScale(image, 1.3, 5)

    # Check again to see if an image was seen
    imageSeen = ( len(faces) != 0 )
    
    # Did we see an image?
    if imageSeen:
        # Put rectangle in every face it picks up
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
            roi_gray = grayImage[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            curTime = time.time()

        # has it been 5 minutes since last play?
        if (curTime ) > lastTime + 5:
            lastTime = curTime
            playSound(decideSound())

    cv2.imshow('Stream',image)

    # Clear the captured frame
    rawCapture.truncate(0)

    # User input to stop (we wait for 'q' key)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cv2.destroyAllWindows()
        break

print("Exiting")
camera.close()
