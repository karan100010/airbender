import os,sys
sys.path.append("/opt/airbender/lib")
from airbender import *
from livdatdatastream import *
a=AirBender("/home/arjun/ids/sks.conf")
a.airveda_login()
time.sleep(10)
airvedafiles=a.airveda_update()
thingspeakfiles=a.thingspeak_update()
avdf=a.airvedadevsheet.worksheet_by_title("Sheet1").get_as_df()
tsdf=a.thingspeakdevsheet.worksheet_by_title("Sheet1").get_as_df()
