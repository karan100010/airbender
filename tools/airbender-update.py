import os,sys
sys.path.append("/opt/airbender/lib")
from airbender import *
from livdatdatastream import *
from ftplib import FTP, error_perm
def placeFiles(ftp, path):
    for name in os.listdir(path):
        localpath = os.path.join(path, name)
        if os.path.isfile(localpath):
            logging.info("STOR", name, localpath)
            ftp.storbinary('STOR ' + name, open(localpath,'rb'))
        elif os.path.isdir(localpath):
            print("MKD", name)

            try:
                ftp.mkd(name)

            # ignore "directory already exists"
            except error_perm as e:
                if not e.args[0].startswith('550'): 
                    raise

            print("CWD", name)
            ftp.cwd(name)
            placeFiles(ftp, localpath)           
            print("CWD", "..")
            ftp.cwd("..")

host="103.21.58.231"
port=21


a=AirBender(sys.argv[1],headless=True)
a.airveda_login()
time.sleep(10)

while True:
	logging.info("Starting update....")
	a.reload_devdf()
	for dev in a.devdf.devname:
		a.update_device(dev)
	ftp=FTP()
	ftp.connect(host,port)
	ftp.login("airbender@environicsindia.in","A1rbender!")
	placeFiles(ftp,"/media/usb/airbenderdata/streamdata/")
	time.sleep(1200)


#airvedafiles=a.airveda_update()
#thingspeakfiles=a.thingspeak_update()

