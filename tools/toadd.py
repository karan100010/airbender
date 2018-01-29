devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
devdatadf=devicedatawsheet.get_as_df()
df.columns=devdatadf.columns
df2=devdatadf.append(df).drop_duplicates()
devicedatawsheet.set_dataframe(df2,(1,1))
history
devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
devdatadf=devicedatawsheet.get_as_df()
df.columns=devdatadf.columns
df2=devdatadf.append(df).drop_duplicates()
devicedatawsheet.set_dataframe(df2,(1,1))
history
devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
devdatadf=devicedatawsheet.get_as_df()
df.columns=devdatadf.columns
df2=devdatadf.append(df).drop_duplicates()
devicedatawsheet.set_dataframe(df2,(1,1))
sks.airveda_update()
sks=SoMACyborg("/home/arjun/ids/sks.conf")
%run airbender-pull-soma.py
sks.airveda_update()
devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
devdatadf=devicedatawsheet.get_as_df()
df.columns=devdatadf.columns
df2=devdatadf.append(df).drop_duplicates()

devicedatawsheet.set_dataframe(df2,(1,1))
cat /home/arjun/ids/sks/SoMASession-2018Jan23-011724/downloads/1211170143.csv
dev
sks.sessiondownloaddir
df
df2
devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
devdatadf=devicedatawsheet.get_as_df()
df.columns=devdatadf.columns
df2=devdatadf.append(df).drop_duplicates()

devicedatawsheet.set_dataframe(df2,(1,1))
devdatasheet.worksheets
devdatasheet.worksheets()
a=devdatasheet.worksheets()
a[0].sheetname
b=a[0]
b.title
for sheets in a:
    sheetnames.append(sheets.title)
sheetnames=[]
sheets=devdatasheet.worksheets()
for sheet in sheets:
    sheetnames.append(sheet.title)
sheetnames
if str(dev) in sheetnames:
    print "Hell"
if str(dev) in sheetnames:
    print "Hell"
    else:
if str(dev) in sheetnames:
    print "Hell"
else:
    devdatasheet.add_worksheet(str(dev))
for dev in devlist.devname:
    if str(dev) in sheetnames:
        print "Sheet exists"
    else:
        print "No sheet"
columns=df.columns
columns=list(df.columns)
for dev in devlist.devname:
    if str(dev) in sheetnames:
        print "Sheet exists"
    else:
        print "No sheet"
        devdatasheet.add_worksheet(str(dev))
        dsheet=devdatasheet.worksheet_by_title(str(dev))
        dsheet.update_row(1,columns)
for dev in devlist.devname:
    if str(dev) in sheetnames:
        print "Sheet exists"
    else:
        print "No sheet"
        devdatasheet.add_worksheet(str(dev))
        dsheet=devdatasheet.worksheet_by_title(str(dev))
        dsheet.update_row(1,columns)
sheetnames=[]
a=devdatasheet.worksheets()
sheets=devdatasheet.worksheets()
for sheet in sheets:
    sheetnames.append(sheet.title)
for dev in devlist.devname:
    if str(dev) in sheetnames:
        print "Sheet exists"
    else:
        print "No sheet"
        devdatasheet.add_worksheet(str(dev))
        dsheet=devdatasheet.worksheet_by_title(str(dev))
        dsheet.update_row(1,columns)
sheets=devdatasheet.worksheets()
sheetnames=[]
for sheet in sheets:
    sheetnames.append(sheet.title)
for dev in devlist.devname:
    if str(dev) in sheetnames:
        print "Sheet exists"
    else:
        print "No sheet"
        devdatasheet.add_worksheet(str(dev))
        dsheet=devdatasheet.worksheet_by_title(str(dev))
        dsheet.update_row(1,columns)
for dev in devlist.devname:
    devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
    df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
    devdatadf=devicedatawsheet.get_as_df()
    df.columns=devdatadf.columns
    df2=devdatadf.append(df).drop_duplicates()
    devicedatawsheet.set_dataframe(df2,(1,1))
dev
df2
df.columns
df.columns
df.columns
dev
for dev in devlist.devname:
    try:
        devicedatawsheet=devdatasheet.worksheet_by_title(str(dev))
        df=pandas.read_csv(os.path.join(sks.sessiondownloaddir,str(dev)+".csv"))
        devdatadf=devicedatawsheet.get_as_df()
        df.columns=devdatadf.columns
        df2=devdatadf.append(df).drop_duplicates()
        devicedatawsheet.set_dataframe(df2,(1,1))
    except:
        print os.path.join(sks.sessiondownloaddir,str(dev)+".csv")
history
