from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import ConfigParser
import time
import os,sys
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

site=login_to_site(abconfig)
devlist=load_dev_list(abdevlist)
