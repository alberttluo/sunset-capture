# sunsetcap.py

import datetime
import time
from suntime import Sun, SunTimeException
import schedule
import json
from urllib.request import urlopen
import cv2

lat = 0
long = 0
cam = cv2.VideoCapture(0)
curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
filename = curr_time + '.jpg'
    
# Get computer location
def getLoc():
    urlopen("http://ipinfo.io/json")
    data = json.load(urlopen("http://ipinfo.io/json"))
    lat = data['loc'].split(',')[0]
    long = data['loc'].split(',')[1]


# Get sunset time daily
def getSSTime():

    sun = Sun(lat, long)

    today_ss = sun.get_sunset_time()

    return(today_ss)

# Take picture of sunset and save to computer
def takePic(cam):
        ret, frame = cam.read()
        cv2.imwrite(filename, frame)
        if ret and frame is not None:
            cam.release()
            cv2.destroyAllWindows()
    
def main():
    while True:
        getLoc()
        getSSTime()
        takePic(cam)
        time.sleep(10)

if __name__ == '__main__':
    main()
    
