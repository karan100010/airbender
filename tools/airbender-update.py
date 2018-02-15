import os,sys
sys.path.append("/opt/airbender/lib")
from airbender import *
from livdatdatastream import *
a=AirBender("/home/arjun/ids/sks.conf")
a.airveda_login()
time.sleep(10)

#airvedafiles=a.airveda_update()
#thingspeakfiles=a.thingspeak_update()

