# sunsetcap.py

import datetime
import time
from suntime import Sun, SunTimeException
import schedule
import json
from urllib.request import urlopen

lat = 0
long = 0

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

schedule.every().day.at("00:00").do(getSSTime)

while True:
    schedule.run_pending()
    time.sleep(1)
