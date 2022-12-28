# sunsetcap.py

import datetime
import time
from suntime import Sun, SunTimeException
import schedule

# Get sunset time daily
def getSSTime():
    latitude = 34.41
    longitude = -118.59

    sun = Sun(latitude, longitude)

    today_ss = sun.get_sunset_time()

    return(today_ss)

schedule.every().day.at("00:00").do(getSSTime)

while True:
    schedule.run_pending()
    time.sleep(1)
