from livdatdatastream import *
def getsipm25(pm25):
	print "PM25: "+str(pm25)
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



def getsipm10(pm10):
	print "PM10: "+str(pm10)
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

def calculate_aqi(row):
	sipm10=getsipm10(float(row['pm10']))
	sipm25=getsipm25(float(row['pm25']))
	if sipm10>sipm25:
		aqi=sipm10
	else:
		aqi=sipm25
	return aqi
	
