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
import bracket_capture

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

        # retry 5 times until we capture an image

        curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        curr_date = datetime.datetime.today()
        newpath = 'images/' + curr_date.strftime('%Y-%m-%d')
        dir = os.path.join(cur_path, newpath)
        if not os.path.exists(dir):
            os.umask(0)
            os.makedirs(dir, mode=0o777)
        bracket_capture.hdr(curr_time, dir)               
                
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
                
            # for testing purposes    
            #today_ss_time = curr_time
            
            print(f"current time: {curr_time}")
            print(f"today sun set time: {today_ss_time}")
            if curr_time < (today_ss_time - timedelta(minutes=10)):
                # command_rtc = 'rtcwake '
                # os.system('rtc') 
                pass
            elif curr_time > (today_ss_time - timedelta(minutes=15)) and curr_time < (today_ss_time + timedelta(minutes=20)):
                takePic()
            
            time.sleep(PIC_INTERVAL)            
        except Exception as e:
            print(f"main ERROR: {e}")

if __name__ == '__main__':
    main()
    
