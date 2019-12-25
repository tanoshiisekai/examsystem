from tools.imagetools import drawwaterprint
import os

filelist = os.listdir(os.getcwd() + "\\problempics")
for f in filelist:
    drawwaterprint(os.getcwd() + "\\problempics\\" + f)
print("finished.")