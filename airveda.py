# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:43:31 2018

@author: k
"""
#two csvs required for this code are insid airbender reposiditory
import pandas as pd
import os
import pygsheets
import shutil
#step1 go in the drive to download df
sheet=pygsheets.authorize("/home/k/client_secret_232033399245-on3oigarcq5a884fkb7gqr9rv9ohef34.apps.googleusercontent.com.json")
devsheet=sheet.open_by_key("1gf4c3_VfR-hUKfhZTOIwyn-uXpcrvbq6ZAV6k9umo_A")
devsheetw1=devsheet.worksheet_by_title("Sheet1")
devdf=devsheetw1.get_as_df()
devdf.head()
#onlyairveda=devicesdf=="airveda"
devicesdf=devdf["devtype"]
#devicesdf
onlyairveda=devicesdf=="airveda"
#onlyairveda
airv=devdf[onlyairveda==True]
names=airv["devname"].tolist()
names
# step 2 renameing columns
df=pd.read_csv("/home/k/to_host/all.csv",index_col=0)
a=pd.read_csv("/home/k/dev/to_host/new_names1.csv")
value=a["CreatedDate.1"].tolist()
key=a["CreatedDate"].tolist()
dictionary = dict(zip(key, value))
df.rename(columns=dictionary,inplace=True)
# step 3 get the csvs separated
for device in names:
    cols = [col for col in df.columns if str(device) in col]
   # print(cols)
    lis=[]
    if len(df[cols].columns !=0):
        df[cols].to_csv("/home/k/test"+str(device)+".csv")
    else:
        lis.append(device)
#step 4 before converting csv _to_json use airbender 
%run dev/airbender/lib/airbender.py   
air=AirBender("airveda.conf")
files=os.listdir("/home/k/all_data/")  
for n in files:
    air.translateairvedadata("/home/k/all_data/"+names)        
#use the function below to convert all csvs to jsons
def csv_to_json(filename):
    a=pd.read_csv(filename,index_col=0)
    path= os.path.splitext(filename)[0]
    b=a.to_json(path+".json",orient='index')
    return b

#step 6 updating in the latest.json file for for each device
        

 
jsons=os.listdir("/home/k/all_data/json/")
folders=os.listdir("/home/k/data/")

for filename in jsons:
    for folder in folders:
        if folder  in filename:
            shutil.copyfile("all_data/json/"+filename,"/home/k/data/"+folder+"/latest.json")
