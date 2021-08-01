#!/usr/bin/env python3
#
# Licensed under the MIT license.  See full license in LICENSE file.
#
# Author: Jarett Rude

from time import sleep
from signal import pause
from datetime import datetime
from picamera import PiCamera
from gpiozero import Button
import shutil
import glob
import subprocess
import os

#Define photo and video directories
picfolder = "/home/pi/LaserCamera/photo/"
timelapsefolder = "/home/pi/LaserCamera/timelapse/"
vidfolder = "/home/pi/LaserCamera/video/"

#Calculate Disk Usage
total, used, free = shutil.disk_usage("/")
#Convert free space from bytes to MB
freeMB = (free // (2**20))
#Define number of MB a Picture is
picsize = 5
#Define maximum number of pictures storage can hold without maxing out
maxpics = ((freeMB // picsize)-1)

#Print to Serial Disk Usage and Max Pictures
print("Total: %d MB" % (total // (2**20)))
print("Used: %d MB" % (used // (2**20)))
print("Free: %d MB" % (free // (2**20)))
print("Max Number of Pictures",maxpics)

#Define starting count of pictures taken
piccount = 0
#Define timelapse interval
interval = 5
#Set recodring state
recording = 0
#Set preview state
laserPreview = 0
#Set video converting state
vidConverting = 0

# DEFINE BUTTONS
redButton = Button(27)
blueButton = Button(5)
yellowButton = Button(7)
blackButton = Button(13)
greenButton = Button(10)
whiteButton = Button(21)

#Define Red Button
def Red():
    camera.stop_preview()
    print("Stop Camera")
#Define Yellow Button
def Yellow():
    global piccount
    global interval
    camera.resolution = (3280, 2464)
    camera.rotation = 180
    print("Start Preview")
    camera.start_preview()
    sleep(2)
    for filename in camera.capture_continuous(timelapsefolder + 'timelapse-{timestamp:%Y-%m-%d-%H-%M-%S}.jpg',use_video_port=False):
        print('Captured %s' % filename)
        piccount = piccount +1
        print(piccount)
        #Stop Timelapse
        if redButton.is_pressed:
            Red()
            break
        sleep(interval)
        if piccount == maxpics:
            print("Storage Full")
            break
#Define Blue Button
def Blue():
    global piccount
    camera.resolution = (3280, 2464)
    camera.rotation = 180
    print("Start Preview")
    camera.start_preview()
    sleep(1)
    now = datetime.now()
    timeStamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    camera.capture(picfolder + 'photo-' + timeStamp + '.jpg')
    print("Photo Taken")
    piccount = piccount +1
    sleep(2)
    camera.stop_preview()
    print(piccount)
#Define Black Button
def Black():
    global recording
    camera.resolution = (1640, 1232)
    camera.rotation = 180
    framerate = (15)
    print("Start Preview")
    camera.start_preview()
    sleep(2)
    now = datetime.now()
    timeStamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    recording = 1
    print("Recording")
    camera.start_recording(vidfolder + 'video-' + timeStamp + '.h264')
    sleep(1)
    while recording == 1:
        camera.wait_recording(0.5)
        if redButton.is_pressed:
            recording = 0
            Red()
#Define File Conversion
def Convert(file_h264, file_mp4):
    command = "MP4Box -add " + file_h264 + " " + file_mp4
    subprocess.run([command], shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
#Define White Button
def White():
    rawVid = glob.glob(vidfolder + "*.h264")
    rawVidNum = len(glob.glob1(vidfolder,"*.h264"))
    convert_count = 0
    while convert_count < rawVidNum:
        print(rawVid[convert_count])
        Convert(rawVid[convert_count] + ":fps=30", os.path.splitext(rawVid[convert_count])[0] + ".mp4")
        sleep(1)
        print("File Converted")
        os.remove(rawVid[convert_count])
        convert_count +=1
    else:
        print("Done")


#lights camera action
while True:
    if greenButton.is_pressed:
        print("Start Preview")
        #define camera configuration
        with PiCamera() as camera:
            camera.rotation = 180
            camera.start_preview()
            sleep(2)
            laserPreview = 1
            while laserPreview == 1:
                #Stop Preivew
                if redButton.is_pressed:
                    laserPreview = 0
                    Red()
                if yellowButton.is_pressed:
                    laserPreview = 0
                    Yellow()
                if blueButton.is_pressed:
                    laserPreview = 0
                    Blue()
                if blackButton.is_pressed:
                    Black()
    if yellowButton.is_pressed:
        with PiCamera() as camera:
            Yellow()
    if blueButton.is_pressed:
        with PiCamera() as camera:
            Blue()
    if blackButton.is_pressed:
        with PiCamera() as camera:
            Black()
    if whiteButton.is_pressed:
        vidConverting = 1
        while vidConverting ==1:
            White()
            sleep(1)
            vidConverting = 0
            break
