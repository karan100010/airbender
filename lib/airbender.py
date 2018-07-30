import os,sys,pandas
sys.path.append("/opt/livingdata/lib")
from livdatbender import *
from livdatdatastream import *
from bs4 import BeautifulSoup
import configparser
# Extend init with *args and **kwargs
		
class AirBender(DataBender):
	def __init__(self,*args, **kwargs):
		super(AirBender,self).__init__(*args, **kwargs)
		self.airvedausername = self.config.get("Airveda","username")
		self.airvedapassword = self.config.get("Airveda","password")
		self.airvedadevicelist = self.config.get("Airveda","devicelist")
		self.airvedaurl = self.config.get("Airveda","airvedaurl")
		self.thingspeakdevicelist = self.config.get("Thingspeak","devicelist")				
		# self.datastreampath=self.config.get("System","datastreampath")
		self.devicelist = self.config.get("Devices","devicelist")				
		
		counter=0
		
		try:
			self.logger.info("Trying to get devsheet")
			self.devsheet=self.gc.open_by_key(self.devicelist)
			self.devdf=self.devsheet.worksheet_by_title("Sheet1").get_as_df()
			self.devdf.devname=self.devdf.devname.apply(str)
			self.devdf.lastupdate=self.devdf.lastupdate.apply(str)
			
		except Exception as e:
			self.logger.error( "Could not get Devsheet " + self.devicelist + " because " + repr(e))
		
		try:
			print "Trying to get airvedadevsheet"
			self.airvedadevsheet=self.gc.open_by_key(self.airvedadevicelist)
			self.avdf=self.airvedadevsheet.worksheet_by_title("Sheet1").get_as_df()
			self.avdf.devname=self.avdf.devname.apply(str)
			self.avdf.lastupdate=self.avdf.lastupdate.apply(str)
			
		except:
			print "Could not get airvedadevsheet " + self.airvedadevicelist
		
		try:
			print "Trying to get thingspeakdevsheet"
			self.thingspeakdevsheet=self.gc.open_by_key(self.thingspeakdevicelist)
			self.tsdf=self.thingspeakdevsheet.worksheet_by_title("Sheet1").get_as_df()
			self.tsdf.devname=self.tsdf.devname.apply(str)
			self.tsdf.lastupdate=self.tsdf.lastupdate.apply(str)
		except:
			print "Could not get thingspeaksheet " + self.thingspeakdevicelist
		
		
		for dev in self.devdf.devname:
			print dev
			ds=DataStream(os.path.join(self.datastreampath,str(dev)),columnnames=['created_at','pm10','pm25','pm1','temp','humidity','entry_id','aqi','co2','batt','airbenderaqi'])
			ds.save_stream()
		'''
		for dev in self.tsdf.devname:
			print dev
			ds=DataStream(os.path.join(self.datastreampath,str(dev)),columnnames=['created_at','pm10','pm25','pm1','temp','humidity','entry_id','aqi','co2','batt','airbenderaqi'])
			ds.save_stream()
		for dev in self.avdf.devname:
			print dev
			ds=DataStream(os.path.join(self.datastreampath,str(dev)),columnnames=['created_at','pm10','pm25','pm1','temp','humidity','entry_id','aqi','co2','batt','airbenderaqi'])
			ds.save_stream()
		'''
	def reload_devdf(self):
		try:
			self.devdf=self.devsheet.worksheet_by_title("Sheet1").get_as_df()
			self.devdf.devname=self.devdf.devname.apply(str)
			self.devdf.lastupdate=self.devdf.lastupdate.apply(str)
		except Exception as exception:
			self.logger.error("Could not reload Dev DF " + repr(exception))
			
			
		try:
			self.tsdf=self.thingspeakdevsheet.worksheet_by_title("Sheet1").get_as_df()
			self.tsdf.devname=self.tsdf.devname.apply(str)
			self.tsdf.lastupdate=self.tsdf.lastupdate.apply(str)
		except Exception as exception:
			print "Could not reload TSDF " + exception
		try:
			self.avdf=self.airvedadevsheet.worksheet_by_title("Sheet1").get_as_df()
			self.avdf.devname=self.avdf.devname.apply(str)
			self.avdf.lastupdate=self.avdf.lastupdate.apply(str)
		except Exception as exception:
			print "Could not reload AVDF " + exception
		#self.devlist=self.avdf.devname.append(self.tsdf.devname).reset_index(drop=True)
			
	def save_devdf(self):
		try:
			self.devsheet.worksheet_by_title("Sheet1").set_dataframe(self.devdf,(1,1))
		except Exception as exception:
			self.logger.error("Could not save Dev DF " + repr(exception))
		
		try:
			self.thingspeakdevsheet.worksheet_by_title("Sheet1").set_dataframe(self.tsdf,(1,1))
		except Exception as exception:
			print "Could not save TSDF " + exception
		try:
			self.airvedadevsheet.worksheet_by_title("Sheet1").set_dataframe(self.avdf,(1,1))
		except Exception as exception:
			print "Could not save AVDF " + exception
	
	def update_devdf(self,devname,field,value):
		dev=self.lookup_device(devname)
		self.devdf.at[dev.name,field]=value
		return True
		if dev['type']=="airveda":
			self.avdf.at[dev['data'].name,field]=value
		if dev['type']=="thingspeak":
			self.tsdf.at[dev['data'].name,field]=value
		return True
	
		
	def lookup_device(self,devname):
		device={}
		try:
			#device['data']=self.devdf.loc[self.devdf.devname==devname].iloc[0]
			#device['type']=device['data'].devtype
			device=self.devdf.loc[self.devdf.devname==devname].iloc[0]
			return device
		except IndexError as exception:
			self.logger.error("Not in  Dev DF")
			return None
		try:
			device['data']=self.tsdf.loc[self.tsdf.devname==devname].iloc[0]
			device['type']="thingspeak"
			return device
		except IndexError as exception:
			print "Not in TSDF"
		try:
			device['data']=self.avdf.loc[self.avdf.devname==devname].iloc[0]
			device['type']="airveda"
			return device
		except IndexError as exception:
			print "Not in AVDF"
		

		
	def airveda_login(self):
		self.goto_url(self.airvedaurl)
		time.sleep(10)
		self.driver.find_element_by_id("txtEmailLogin").send_keys(self.airvedausername)
		self.driver.find_element_by_id("txtPasswordLogin").send_keys(self.airvedapassword)
		self.driver.find_element_by_id("txtPasswordLogin").send_keys(Keys.RETURN)
	
	def airveda_get_dev_data(self,row):
		dev=row.devname
		if os.path.exists(os.path.join(self.sessiondownloaddir,str(dev)+".csv")):
			os.rename(os.path.join(self.sessiondownloaddir,str(dev)+".csv"),os.path.join(self.sessiondownloaddir,str(dev)+"-prev.csv"))
		"""self.goto_url(self.airvedaurl)
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
		time.sleep(20)"""
		os.rename(os.path.join(self.sessiondownloaddir,"airveda_data.csv"),os.path.join(self.sessiondownloaddir,str(dev)+".csv"))
		return os.path.join(self.sessiondownloaddir,str(dev)+".csv")
	
	def thingspeak_get_dev_data(self,row):
		latestjson=json.loads(urllib2.urlopen(row.url+"/feed.json").read())
		filepath=os.path.join(self.sessiondownloaddir,row.devname+".json")
		if os.path.exists(os.path.join(self.sessiondownloaddir,row.devname+".json")):
			os.rename(os.path.join(self.sessiondownloaddir,row.devname+".json"),os.path.join(self.sessiondownloaddir,row.devname+"-prev.json"))
		with open(filepath,"w") as f:
			f.write(json.dumps(latestjson))
		print filepath
		return filepath
	'''		
	
	def update_device(self,devname):
		downloadedfile=None
		dev=self.lookup_device(devname)
		print dev
		print dev.devtype
		row=dev
		print row.devname
		ds=DataStream(os.path.join(self.datastreampath,str(row.devname)),columnnames=['created_at','pm10','pm25','pm1','temp','humidity','entry_id','aqi','co2','batt','airbenderaqi'])
		ds.save_stream()
		tsval=datetime.now()
		remark="Trying update at " + tsval.strftime("%Y-%m-%d %H:%M:%S")
		self.update_devdf(row.devname,"remarks",remark)
		try:
			if dev.devtype=="airveda":
				devfile = self.airveda_get_dev_data(row)
			if dev.devtype=="thingspeak":
				devfile=self.thingspeak_get_dev_data(row)
			downloadedfile=devfile
			print devfile
			tsval=datetime.now()
			remark="Successful download at " + tsval.strftime("%Y-%m-%d %H:%M:%S")
			self.update_devdf(row.devname,"remarks",remark)
			self.update_devdf(row.devname,"localfile",devfile)
			if dev.devtype=="airveda":
				cdata=self.translateairvedadata(devfile)
			if dev.devtype=="thingspeak":
				cdata=self.translatethingspeakdata(devfile)
			cdata=self.add_airbender_aqi_column(cdata)
			lastupdate=cdata.at[len(cdata)-1,"created_at"].strftime("%Y-%m-%d %H:%M:%S")
			airbenderaqi=cdata.at[len(cdata)-1,"airbenderaqi"]
			print "Last update at", lastupdate
			self.update_devdf(row.devname,"lastupdate",lastupdate)
			self.update_devdf(row.devname,"aqi",airbenderaqi)
			ds.append_data(cdata)
			ds.save_stream()
		except Exception as exception:
			print exception
			tsval=datetime.now()
			remark="Failed download at " + tsval.strftime("%Y-%m-%d %H:%M:%S")
			self.update_devdf(row.devname,"remarks",remark)
		self.save_devdf()
		return downloadedfile
    '''
	
	
	'''
	def airveda_update_device(self,avdfrow):
		downloadedfile=None
		row=avdfrow
		print row.devname
		ds=DataStream(os.path.join(self.datastreampath,str(row.devname)),columnnames=['created_at','pm10','pm25','pm1','temp','humidity','entry_id','aqi','co2','batt','airbenderaqi'])
		ds.save_stream()
		tsval=datetime.now()
		remark="Trying update at " + tsval.strftime("%Y-%m-%d %H:%M:%S")
		self.update_df(row.devname,"remarks",remark)
		try:
			devfile = self.airveda_get_dev_data(row)
			downloadedfile=devfile
			print devfile
			tsval=datetime.now()
			remark="Successful download at " + tsval.strftime("%Y-%m-%d %H:%M:%S")
			self.update_df(row.devname,"remarks",remark)
			self.update_df(row.devname,"localfile",devfile)
			cdata=self.translateairvedadata(devfile)
			cdata=self.add_airbender_aqi_column(cdata)
			lastupdate=cdata.at[len(cdata)-1,"created_at"].strftime("%Y-%m-%d %H:%M:%S")
			print "Last update at", lastupdate
			self.update_df(row.devname,"lastupdate",lastupdate)
			ds.append_data(cdata)
			ds.save_stream()
		except Exception as exception:
			print exception
			tsval=datetime.now()
			remark="Failed download at " + tsval.strftime("%Y-%m-%d %H:%M:%S")
			self.update_df(row.devname,"remarks",remark)
		self.save_dfs()
		return downloadedfile
	
	def thingspeak_update_device(self,tsdfrow):
		downloadedfile=None
		row=tsdfrow
		print row.devname
		ds=DataStream(os.path.join(self.datastreampath,str(row.devname)),columnnames=['created_at','pm10','pm25','pm1','temp','humidity','entry_id','aqi','co2','batt','airbenderaqi'])
		ds.save_stream()
		tsval=datetime.now()
		remark="Trying update at " + tsval.strftime("%Y-%m-%d %H:%M:%S")
		self.update_df(row.devname,"remarks",remark)
		try:
			devfile=self.thingspeak_get_dev_data(row)
			downloadedfile=filepath
			tsval=datetime.now()
			remark="Successful download at " + tsval.strftime("%Y-%m-%d %H:%M:%S")
			self.update_df(row.devname,"remarks",remark)
			self.update_df(row.devname,"localfile",filepath)
			cdata=self.translatethingspeakdata(filepath)
			cdata=self.add_airbender_aqi_column(cdata)
			lastupdate=cdata.at[len(cdata)-1,"created_at"].strftime("%Y-%m-%d %H:%M:%S")
			print "Last update at", lastupdate
			self.update_df(row.devname,"lastupdate",lastupdate)
			ds.append_data(cdata)
			ds.save_stream()
		except Exception as exception:
			print exception
			tsval=datetime.now()
			remark="Failed download at " + tsval.strftime("%Y-%m-%d %H:%M:%S")
			self.update_df(row.devname,"remarks",remark)
		self.save_dfs()
		return downloadedfile
	'''
	def translateairvedadata(self,channelfile):
		try:
			channelfiledata=pandas.read_csv(channelfile,parse_dates=True)
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
		channeldata.created_at=channeldata.created_at.apply(pandas.to_datetime)
		channeldata.pm10=channeldata.pm10.apply(pandas.to_numeric)
		channeldata.pm25=channeldata.pm25.apply(pandas.to_numeric)
		channeldata.pm1=channeldata.pm1.apply(pandas.to_numeric)
		channeldata.temp=channeldata.temp.apply(pandas.to_numeric)
		channeldata.aqi=channeldata.aqi.apply(pandas.to_numeric)
		channeldata=self.add_airbender_aqi_column(channeldata)
		return channeldata
	
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
		for feed in feeds:
			row={}
			row['created_at']=feed['created_at']
			row['entry_id']=feed['entry_id']
			for key in feed.keys():
				
				if key.startswith("field"):
					if channeldef[key] in channeldata.columns:
						row[channeldef[key]]=feed[key]
			
			channeldata=channeldata.append([row],ignore_index=True).drop_duplicates()
		channeldata.created_at=channeldata.created_at.apply(pandas.to_datetime)
		channeldata.pm10=channeldata.pm10.apply(pandas.to_numeric)
		channeldata.pm25=channeldata.pm25.apply(pandas.to_numeric)
		channeldata.pm1=channeldata.pm1.apply(pandas.to_numeric)
		channeldata.temp=channeldata.temp.apply(pandas.to_numeric)
		channeldata.aqi=channeldata.aqi.apply(pandas.to_numeric)
		channeldata=self.add_airbender_aqi_column(channeldata)
		return channeldata
	
	def airveda_update(self):
		downloadedfiles={}
		for index,row in self.avdf.iterrows():
			downloadedfile=self.airveda_update_device(row)
			downloadedfiles[row.devname]=downloadedfile
		return downloadedfiles
	
	def thingspeak_update(self):
		downloadedfiles={}
		for index,row in self.tsdf.iterrows():
			downloadedfile=self.thingspeak_update_device(row)
			downloadedfiles[row.devname]=downloadedfile
		return downloadedfiles
	
	def getsipm25(self,pm25):
		#print "PM25: "+str(pm25)
		if pm25<=30:
			return pm25*50/30
		elif pm25>30 and pm25<=60:
			return 50+(pm25-30)*50/30

		elif pm25>60 and pm25<=90:
			return 100+(pm25-60)*100/30
					
		elif pm25>90 and pm25<=120:
			return 200+(pm25-90)*(100/30)

		elif pm25>120 and pm25<=250:
			return 300+(pm25-120)*(100/130)

		elif pm25>250:
			return 400+(pm25-250)*(100/130)

	def getsipm10(self,pm10):
		#print "PM10: "+str(pm10)
		if pm10<=50:
			return pm10

		elif pm10>50 and pm10<=100:
			return pm10

		elif pm10>100 and pm10<=250:
			return 100+(pm10-100)*100/150
		
		elif pm10>250 and pm10<=350:
			return 200+(pm10-250)

		elif pm10>350 and pm10<=430:
			return 300+(pm10-350)*(100/80)

		elif pm10>430:
			return 400+(pm10-430)*(100/80)
			
	def calculate_aqi(self,row):
		sipm10=self.getsipm10(float(row['pm10']))
		sipm25=self.getsipm25(float(row['pm25']))
		if sipm10>sipm25:
			aqi=sipm10
		else:
			aqi=sipm25
		return aqi	
	
	def add_airbender_aqi_column(self,cdata):
		cdata['airbenderaqi']=cdata.apply(lambda row: self.calculate_aqi(row),axis=1)
		cdata.airbenderaqi=cdata.airbenderaqi.apply(pandas.to_numeric)
		
		return cdata
