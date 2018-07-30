#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 09:53:20 2018

@author: lilhack110
"""

import os,sys
sys.path.append("/opt/livingdata/lib")
from livdatbender1 import *
import ConfigParser
import pygsheets
def get_airveda(gc,conf_file):
    config=ConfigParser.ConfigParser()
    config.read(conf_file)
    airvedausername= config.get("Airveda","username")
    airvedapassword=config.get("Airveda","password")
    airvedadevicelist=config.get("Airveda","devicelist")
    airvedaurl=config.get("Airveda","devicelist")
    thingspeakdevicelist = config.get("Thingspeak","devicelist")
    #datastreampath=config.get("System","datastreampath")
    devicelist = config.get("Devices","devicelist")
    try:
        #self.logger.info("Trying to get devsheet")
        devsheet=gc.open_by_key(devicelist)
        devdf=devsheet.worksheet_by_title("Sheet1").get_as_df()
        devdf.devname=devdf.devname.apply(str)
        devdf.lastupdate=devdf.lastupdate.apply(str)
        return devdf
    except Exception as e:
        #logger.error( "Could not get Devsheet " + self.devicelist + " because " + repr(e))
        print("Could not get Devsheets")
        

def thingspeaksheet():		
		try:
			print "Trying to get thingspeakdevsheet"
			thingspeakdevsheet=gc.open_by_key(thingspeakdevicelist)
			tsdf=thingspeakdevsheet.worksheet_by_title("Sheet1").get_as_df()
			tsdf.devname=tsdf.devname.apply(str)
			tsdf.lastupdate=tsdf.lastupdate.apply(str)
		except:
			print "Could not get thingspeaksheet " + thingspeakdevicelist
		
		
		for dev in devdf.devname:
			print dev
			ds=DataStream(os.path.join(datastreampath,str(dev)),columnnames=['created_at','pm10','pm25','pm1','temp','humidity','entry_id','aqi','co2','batt','airbenderaqi'])
			ds.save_stream()        