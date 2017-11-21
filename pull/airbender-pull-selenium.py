from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import ConfigParser
import time
import os,sys,json,geojson,urllib
sys.path.append("/opt/livingdata/lib")
from livdatcsvlib import *

abconfig="/home/arjun/ids/airbender/gkbhat.conf"
abdevlist="/home/arjun/dev/airbender/web/data/devlist.csv"
def setup(configfile):
	config=ConfigParser.ConfigParser()
	config.read(configfile)
	return config
	
def login_to_site(configfile):
	config=setup(configfile)
	usr = config.get("User","username")
	pwd = config.get("User","password")
	url = config.get("Site","url")
	sitel_username = config.get("Site","sitel_username")
	sitel_pw = config.get("Site","sitel_pw")
	firefox_profile = webdriver.FirefoxProfile()
	firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
	driver = webdriver.Firefox(firefox_profile=firefox_profile)
	# or you can use Chrome(executable_path="/usr/bin/chromedriver")
	driver.get(url)
	elem = driver.find_element_by_id("sign_in_email")
	elem.send_keys(usr)
	elem=driver.find_element_by_id("checkEmail")
	elem.click()
	time.sleep(2)
	elem = driver.find_element_by_id("user_password")
	elem.send_keys(pwd)
	time.sleep(2)
	elem=driver.find_element_by_id("sign_in")
	elem.click()
	return driver
	#elem.send_keys(Keys.RETURN)

def load_dev_list(devlistfile):
	devlist=CSVFile()
	devlist.importfile(devlistfile)
	return devlist


def get_all_feed_json(devlist):
	config=setup(abconfig)
	datapath=config.get("Data","datapath")
	for dev in devlist.matrix:
		filename= urllib.URLopener()
		try:
			print "Trying to get JSON for %s" %dev['DevName']
			filename.retrieve(dev['URL']+"/feed.json",os.path.join(datapath,"%s.json" %dev['Folder']))
		except:
			print "Couldnt get feed for %s" %dev['DevName']
def get_all_feed_csv(devlist):
	config=setup(abconfig)
	datapath=config.get("Data","datapath")
	for dev in devlist.matrix:
		filename= urllib.URLopener()
		try:
			print "Trying to get CSV for %s" %dev['DevName']
			filename.retrieve(dev['URL']+"/feeds.csv",os.path.join(datapath,"%s.csv" %dev['Folder']))
		except:
			print "Couldnt get feed for %s" %dev['DevName']


def set_lat_long_for_devices(devlist):
	config=setup(abconfig)
	datapath=config.get("Data","datapath")
	geodevlist=[]
	for dev in devlist.matrix:
		jsonfile=os.path.join(datapath,"%s.json" %dev['Folder'])
		f=open(jsonfile,"r")
		devjson=json.loads(f.read())
		f.close()
		#latitude=devjson['channel']['latitude']
		#longitude=devjson['channel']['longitude']
		latitude=devjson['feeds'][0]['field6']
		longitude=devjson['feeds'][0]['field7']
		
		geodev={}
		for col in devlist.colnames:
			geodev[col]=dev[col]
		geodev['latitude']=latitude
		geodev['longitude']=longitude
		geodevlist.append(geodev)
	c=CSVFile()
	c.colnames=devlist.colnames
	c.matrix=geodevlist
	return c
	#c.exportfile(abdevlist)
	

	
#site=login_to_site(abconfig)
def get_data():
	get_all_feed_json(devlist)
	get_all_feed_csv(devlist)
	
def get_devmarkerfc(devlist):
	devicemarkers=[]
	for dev in devlist.matrix:
		feature=geojson.Feature()
		print dev['latitude']
		point=geojson.Point((float(dev['longitude']),float(dev['latitude'])))
		feature['geometry']=point
		for colname in devlist.colnames:
			feature['properties'][colname]=dev[colname]
		devicemarkers.append(feature)
	devicemarkersfc=geojson.FeatureCollection(devicemarkers)
	return devicemarkersfc
devlist=load_dev_list(abdevlist)
