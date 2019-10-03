
import os
dbconnection = 'sqlite:///db/examsystem.db'

buildhost = "192.168.2.210"
buildport = "9100"

baseurl = "http://" + buildhost + ":" + buildport

extvalid = ['zip']

problempicdir = "problempics"

tempdirname = "problems"
tempfilename = "temp.zip"
importpath = "temp"

dataxlsxname = "problems.xlsx"
datapicdir = "pics"

fileserverip = "192.168.2.210"
fileserverport = "9101"

filebasedir = "filebasedir"
filebasefilename = "problems.zip"

if not os.path.exists(importpath):
    os.mkdir(importpath)
