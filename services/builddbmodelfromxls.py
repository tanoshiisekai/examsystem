from pyexcel_xlsx import get_data
import os

tablength = 4

wb = get_data(os.getcwd() + "/数据库设计.xlsx")
ws = wb["数据库设计"]
fp = ""
filestr = ""
flag = 0
itemlist = []
for line in ws:
    if len(line) == 0 and flag == 0:
        continue
    if len(line) == 0 and flag == 1:
        filestr = filestr + " " * tablength + "def __init__(self, "
        for item in itemlist:
            filestr = filestr + item + ","
        filestr = filestr[:-1] + "):\n"
        for item in itemlist:
            filestr = filestr + " " * tablength + " " * \
                tablength + "self." + item + " = " + item + "\n"
        filestr = filestr + " " * tablength + "def todict(self):\n"
        filestr = filestr + " " * tablength + " " * tablength + "return {"
        for item in itemlist:
            filestr = filestr + '"' + item + '":' + "self." + item + ",\n"
        filestr = filestr[:-2] + "}"
        fp.write(filestr)
        fp.close()
        flag = 0
        itemlist = []
        continue
    if line[0] == "英文表名":
        flag = 1
        tablename = line[1]
        fp = open(os.getcwd() + "/dbmodels/" +
                  tablename.lower() + "DBModel.py", "w")
        filestr = "from appbase import global_db as gdb\nclass "
        filestr = filestr + tablename + "(gdb.Model):\n"
        filestr = filestr + " " * tablength
        filestr = filestr + "__tablename__ = '" + tablename.lower() + "'\n"
    elif line[0] == "英文列名":
        continue
    else:
        pkey = False
        cname = line[0]
        ctype = line[2]
        itemlist.append(cname)
        if len(line) > 3:
            if line[3] == "是":
                pkey = True
            else:
                pkey = False
        if pkey == True:
            filestr = filestr + " " * tablength + cname + \
                " = gdb.Column(gdb." + ctype + ", primary_key=True)\n"
        else:
            filestr = filestr + " " * tablength + cname + \
                " = gdb.Column(gdb." + ctype + ")\n"
else:
    filestr = filestr + " " * tablength + "def __init__(self, "
    for item in itemlist:
        filestr = filestr + item + ","
    filestr = filestr[:-1] + "):\n"
    for item in itemlist:
        filestr = filestr + " " * tablength + " " * \
            tablength + "self." + item + " = " + item + "\n"
    filestr = filestr + " " * tablength + "def todict(self):\n"
    filestr = filestr + " " * tablength + " " * tablength + "return {"
    for item in itemlist:
        filestr = filestr + '"' + item + '":' + "self." + item + ",\n"
    filestr = filestr[:-2] + "}"
    fp.write(filestr)
    fp.close()
