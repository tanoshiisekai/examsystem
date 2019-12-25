
import os
dbconnection = 'sqlite:///db/examsystem.db'

buildhost = "192.168.31.254"
buildport = "9100"

fileserverip = "192.168.31.254"
fileserverport = "9101"

apiversion = "0.3"   # 修改代码后，修改代码版本号，以刷新前端浏览器

baseurl = "http://" + buildhost + ":" + buildport

extvalid = ['zip']

problempicdir = "problempics"

tempdirname = "problems"
tempfilename = "temp.zip"
importpath = "temp"

dataxlsxname = "problems.xlsx"
datapicdir = "pics"

filebasedir = "filebasedir"
filebasefilename = "problems.zip"

if not os.path.exists(importpath):
    os.mkdir(importpath)
