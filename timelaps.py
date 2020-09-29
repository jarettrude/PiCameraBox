from time import sleep
from picamera import PiCamera
import shutil
import sys

#Variables
#Define photo directory
picfolder = "/home/pi/Pictures"
#Calculate Disk Usage
total, used, free = shutil.disk_usage("/")
#Convert free space from bytes to MB
freeMB = (free // (2**20))
#Define number of MB a Picture is
picsize = 4
#Define maximum number of pictures storage can hold without maxing out
maxpics = ((freeMB // picsize)-1)
#Define camera
camera = PiCamera()
#Define resolution
camera.resolution = (2592, 1944)
#Define starting count of pictures taken
piccount = 0

#Print to Serial Disk Usage and Max Pictures
print("Total: %d MB" % (total // (2**20)))
print("Used: %d MB" % (used // (2**20)))
print("Free: %d MB" % (free // (2**20)))
print("Max Number of Pictures",maxpics)

#Take Timelapse
for filename in camera.capture_continuous(picfolder + '/' + 'img{counter:09d}.jpg'):
    print('Captured %s' % filename)
    piccount = piccount +1
    print(piccount)
    sleep(2) # wait 2 seconds
    if piccount == maxpics:
        sys.exit()
