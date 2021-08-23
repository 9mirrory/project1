import datetime
from time import sleep

time_now = datetime.datetime.now()

day = str(input())

hour = str(input())

minutes = str(input())

if len(day) == 1:
    day = '0' + day
if len(hour) == 1:
    hour = '0' + hour
if len(minutes) == 1:
    minutes = '0' + minutes
while True:
    time_now = datetime.datetime.now()
    if str(time_now.hour) == hour and str(time_now.minute) == minutes and str(time_now.day) == day:
        break
    sleep(1)