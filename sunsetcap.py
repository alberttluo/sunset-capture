# sunsetcap.py

import datetime
from datetime import date, timedelta, timezone
import time
from suntime import Sun, SunTimeException
import schedule
import json
from urllib.request import urlopen
import cv2
import os
import pathlib

cur_path = pathlib.Path(__file__).parent.resolve()


SUN_SET_CONFIG = os.path.join(cur_path, 'config/sun_set_config.json')
NUM_PICS = 10
PIC_INTERVAL = 60  #seconds

# Get computer location
def getLoc():
    urlopen("http://ipinfo.io/json")
    data = json.load(urlopen("http://ipinfo.io/json"))
    lat = data['loc'].split(',')[0]
    long = data['loc'].split(',')[1]
    return lat, long

# Get sunset time daily
def getSSTime(lat, long):
    sun = Sun(float(lat), float(long))
    today_ss = sun.get_local_sunset_time()
    print("Today sun set time loaded from internet: ", today_ss)
    
    jdata = {}
    jdata['Latitude'] = lat
    jdata['Longitude'] = long
    jdata['TodaySunSetTime'] = today_ss.strftime('%H:%M:%S')
    
    with open(SUN_SET_CONFIG, 'w') as f:
        json.dump(jdata, f, indent=4, default=str)

    return today_ss

# Take picture of sunset and save to computer
def takePic():
    try:
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)
        
        # retry 5 times until we capture an image
        retry = 5
        while(retry > 0):
            curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            curr_date = datetime.datetime.today()
            newpath = 'images/' + curr_date.strftime('%Y-%m-%d')
            dir = os.path.join(cur_path, newpath)
            if not os.path.exists(dir):
                os.umask(0)
                os.makedirs(dir, mode=0o777)

            filename = dir + '/' + curr_time + '.jpg'
            ret, frame = cam.read()
            if ret:
                cv2.imwrite(filename, frame)
                print(f"captured one image: {filename}")
                break
            retry -= 1
            
        cam.release()
    except Exception as e:
        print(f"takePic ERROR: {e}")

def main():

    num_pics = 0

    while True:
        curr_time = datetime.datetime.now()
        try:
            lat, long = getLoc()
            today_ss = getSSTime(lat, long)
        except Exception as e:
            # read from the config file (json)
            with open(SUN_SET_CONFIG, 'r') as f:
                data = json.load(f)
                today_ss = datetime.datetime.strptime(
                    curr_time.strftime('%Y-%m-%d') + " " + data['TodaySunSetTime'], '%Y-%m-%d %H:%M:%S')
                print(f"sun set time loaded from file: {today_ss}")
        try:
            today_ss_time = datetime.datetime.strptime(
                curr_time.strftime('%Y-%m-%d') + " " + today_ss.strftime('%H-%M-%S'), '%Y-%m-%d %H-%M-%S')
            today_ss_time = curr_time
            
            print(f"current time: {curr_time}")
            print(f"today sun set time: {today_ss_time}")
            if curr_time < (today_ss_time - timedelta(minutes=5)):
                # command_rtc = 'rtcwake '
                # os.system('rtc') 
                pass
            elif curr_time > (today_ss_time - timedelta(minutes=5)) and curr_time < (today_ss_time + timedelta(minutes=20)):
                takePic()
            
            time.sleep(PIC_INTERVAL)            
        except Exception as e:
            print(f"main ERROR: {e}")

if __name__ == '__main__':
    main()
    
