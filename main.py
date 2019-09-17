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
    return fileList[random.randrange(0,len(fileList))]

def playSound(soundFile):
    pygame.mixer.music.load(soundFile)
    pygame.mixer.music.play()

# Initialize the camera and camera capture
camera = picamera.PiCamera()
rawCapture = picamera.array.PiRGBArray(camera, size=(800,608))

# Initialize pygame which will be used to play audio
pygame.init()

#camera.resolution = (640,480)
camera.resolution = (800,608)
camera.vflip = False
camera.hflip = False
camera.framerate = 15
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
            small = cv2.imread("./flairFaces/ricFlairFace.jpg",-1)
            resized = cv2.resize(small,(w,h))

            #Copy because image is read-only array
            image2 = image.copy()

            # Remove Black TODO
            # Doesn't work correctly, makes too light and see through
            #alphaSmall = resized / 255.0
            #alphaImage = 1.0 - alphaSmall
            #image2[y:y+h,x:x+w] = (alphaSmall * resized[:,:] + alphaImage * image2[y:y+h,x:x+w])

            image2[y:y+h,x:x+w] = resized
            #Set Image to be displayed
            image = image2
            curTime = time.time()

        # has it been 7 seconds since last play?
        if (curTime ) > lastTime + 10:
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
