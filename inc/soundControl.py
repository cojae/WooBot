# This might be overkill, but this library will do the audio playing
# Perhaps find one that isn't as expansive as this one
import pygame
import random

import os

def decideSound(dir_path):
    retString = ""
    soundsDir = dir_path + "/sounds/"
    #fileList = [os.path.join(dir_path,"/sounds/",f) for f in os.listdir(dir_path+"/sounds")]
    fileList = [os.path.join(soundsDir,f) for f in os.listdir(dir_path+"/sounds")]
    return fileList[random.randrange(0,len(fileList))]

def playSound(soundFile):
    pygame.mixer.music.load(soundFile)
    pygame.mixer.music.play()
