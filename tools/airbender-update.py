import os,sys
sys.path.append("/opt/airbender/lib")
from airbender import *
from livdatdatastream import *
from ftplib import FTP, error_perm
def placeFiles(ftp, path):
    for name in os.listdir(path):
        localpath = os.path.join(path, name)
        if os.path.isfile(localpath):
            print("STOR", name, localpath)
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



a=AirBender(sys.argv[1],headless=True)
a.airveda_login()
time.sleep(10)


for dev in a.devdf.devname:
    a.update_device(dev)


host="103.21.58.231"
port=21
ftp=FTP()
ftp.connect(host,port)
ftp.login("airbender@environicsindia.in","A1rbender!")
placeFiles(ftp,"/media/usb/airbenderdata/streamdata/")



#airvedafiles=a.airveda_update()
#thingspeakfiles=a.thingspeak_update()

