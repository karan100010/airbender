import os,sys

sys.path.append("/opt/livingdata/lib")
sys.path.append("/opt/SoMA/python/lib")
from livdatbutler import *
from libsoma import *

from bs4 import BeautifulSoup

# Extend init with *args and **kwargs

class AirBender(DataButler):
	def __init__(self,*args, **kwargs):
		super(AirBender,self).__init__(*args, **kwargs)
		self.airvedausername = self.config.get("Airveda","username")
		self.airvedapassword = self.config.get("Airveda","password")
		self.airvedadevicelist = self.config.get("Airveda","devicelist")
		counter=0
		try:
			print "Trying to get airvedadevsheet"
			self.airvedadevsheet=self.gc.open_by_key(self.airvedadevicelist)
		except:
			counter +=1
			
		
	def airveda_get_dev_data(self,dev):
		if os.path.exists(os.path.join(self.sessiondownloaddir,str(dev)+".csv")):
			os.rename(os.path.join(self.sessiondownloaddir,str(dev)+".csv"),os.path.join(self.sessiondownloaddir,str(dev)+"-prev.csv"))
		self.goto_url("http://api.airveda.com/core/download/")
		time.sleep(10)
		self.driver.find_element_by_id("checkbox2").click()
		self.driver.find_element_by_id("checkbox3").click()
		self.driver.find_element_by_id("checkbox4").click()
		self.driver.find_element_by_id("checkbox5").click()
		self.driver.find_element_by_id("checkbox6").click()
		self.driver.find_element_by_name("average").click()
		self.driver.find_element_by_class_name("select2-search__field").click()
		self.driver.find_element_by_class_name("select2-search__field").send_keys(dev)
		self.driver.find_element_by_class_name("select2-search__field").send_keys(Keys.RETURN)
		time.sleep(3)
		self.driver.find_element_by_id("download_button").click()
		time.sleep(20)
		os.rename(os.path.join(self.sessiondownloaddir,"airveda_data.csv"),os.path.join(self.sessiondownloaddir,str(dev)+".csv"))
		return os.path.join(self.sessiondownloaddir,str(dev)+".csv")
	def airveda_update(self):
		devsheetdf=self.airvedadevsheet.worksheet_by_title("Sheet1").get_as_df()
		for dev in devsheetdf.devname:
			print self.airveda_get_dev_data(dev)
	
if __name__=="__main__":
	airvedaurl="http://api.airveda.com/core/download/"
	sks=AirBender("/home/arjun/ids/sks.conf",headless=False)
	sks.goto_url("http://api.airveda.com/core/download/")
	time.sleep(10)
	sks.driver.find_element_by_name("username").send_keys(sks.airvedausername)
	sks.driver.find_element_by_name("password").send_keys(sks.airvedapassword)
	sks.driver.find_element_by_name("username").send_keys(Keys.RETURN)
		


