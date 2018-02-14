import os,sys,pandas
sys.path.append("/opt/livingdata/lib")
from livdatbender import *
from livdatdatastream import *
from bs4 import BeautifulSoup

# Extend init with *args and **kwargs
		
class AirBender(DataBender):
	def __init__(self,*args, **kwargs):
		super(AirBender,self).__init__(*args, **kwargs)
		self.airvedausername = self.config.get("Airveda","username")
		self.airvedapassword = self.config.get("Airveda","password")
		self.airvedadevicelist = self.config.get("Airveda","devicelist")
		self.airvedaurl = self.config.get("Airveda","airvedaurl")
		self.thingspeakdevicelist = self.config.get("Thingspeak","devicelist")				
		counter=0
		try:
			print "Trying to get airvedadevsheet"
			self.airvedadevsheet=self.gc.open_by_key(self.airvedadevicelist)
		except:
			print "Could not get airvedadevsheet " + self.airvedadevicelist
	
		try:
			print "Trying to get thingspeakdevsheet"
			self.thingspeakdevsheet=self.gc.open_by_key(self.thingspeakdevicelist)
		except:
			print "Could not get thingspeaksheet " + self.thingspeakdevicelist
	
	def airveda_login(self):
		self.goto_url(self.airvedaurl)
		time.sleep(10)
		self.driver.find_element_by_name("username").send_keys(self.airvedausername)
		self.driver.find_element_by_name("password").send_keys(self.airvedapassword)
		self.driver.find_element_by_name("username").send_keys(Keys.RETURN)
	
	
	def airveda_get_dev_data(self,dev):
		if os.path.exists(os.path.join(self.sessiondownloaddir,str(dev)+".csv")):
			os.rename(os.path.join(self.sessiondownloaddir,str(dev)+".csv"),os.path.join(self.sessiondownloaddir,str(dev)+"-prev.csv"))
		self.goto_url(self.airvedaurl)
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
		downloadedfiles={}
		for dev in devsheetdf.devname:
			devfile = self.airveda_get_dev_data(dev)
			downloadedfiles[dev]=devfile
			print devfile
		return downloadedfiles
	
	def thingspeak_update(self):
		devsheetdf=self.thingspeakdevsheet.worksheet_by_title("Sheet1").get_as_df()
		downloadedfiles={}
		for index,row in devsheetdf.iterrows():
			latestjson=json.loads(urllib2.urlopen(row['url']+"/feed.json").read())
			filepath=os.path.join(self.sessiondownloaddir,row['devname']+".json")
			if os.path.exists(os.path.join(self.sessiondownloaddir,row['devname']+".json")):
				os.rename(os.path.join(self.sessiondownloaddir,row['devname']+".json"),os.path.join(self.sessiondownloaddir,row['devname']+"-prev.json"))
			with open(filepath,"w") as f:
				f.write(json.dumps(latestjson))
			print filepath
			downloadedfiles[row['devname']]=filepath
		return downloadedfiles
	
	def translatethingspeakdata(self,channelfile):
		with open(channelfile,"r") as f:
			channeljson=json.loads(f.read())
		channeldata=pandas.DataFrame(columns=['created_at','pm10','pm25','pm1','temp','humidity','entry_id','aqi','co2','batt'])
		channeldef=channeljson['channel']
		#print channeldef
		for defn in channeldef.keys():
			if channeldef[defn]=='Dust_PM25' or  channeldef[defn]=='PM2.5' or channeldef[defn]=='PM 2.5':
				channeldef[defn]='pm25'
			if channeldef[defn]=='Dust_PM10' or channeldef[defn]=='PM 10':
				channeldef[defn]='pm10'
			if channeldef[defn]=='Dust_PM01' or channeldef[defn]=='PM 1' or channeldef[defn]== 'PM 01':
				channeldef[defn]='pm1'
			if channeldef[defn]=='TEMPERATURE' or channeldef[defn]=='Temp C':
				channeldef[defn]='temp'
			if channeldef[defn]=='HUMIDITY' or channeldef[defn]=='Humidity':
				channeldef[defn]='humid'
			if channeldef[defn]=='BATTERY' or channeldef[defn]=='BattVolt'  or channeldef[defn]=='BATTERY' or channeldef[defn]=='Bat mV':
				channeldef[defn]='batt'
		feeds=channeljson['feeds']
		print channeldef
		
		for feed in feeds:
			row={}
			row['created_at']=feed['created_at']
			row['entry_id']=feed['entry_id']
			for key in feed.keys():
				
				if key.startswith("field"):
					if channeldef[key] in channeldata.columns:
						row[channeldef[key]]=feed[key]
			
			channeldata=channeldata.append([row],ignore_index=True).drop_duplicates()
		return channeldata
	def translateairvedadata(self,channelfile):
		try:
			channelfiledata=pandas.read_csv(channelfile)
		except:
			print "Could not read file " + channelfile
			return None
		cfdata=pandas.DataFrame(columns=["created_at","pm25","pm10","aqi","co2"])
		if len(cfdata.columns)!=len(channelfiledata.columns):
			print "Column mismatch in file " + channelfile
			return None
		channelfiledata.columns=cfdata.columns
		channeldata=pandas.DataFrame(columns=['created_at','pm10','pm25','pm1','temp','humidity','entry_id','aqi','co2','batt'])
		channeldata=channeldata.append(channelfiledata).drop_duplicates()
		return channeldata
