import os
import json
import logging
from zipfile import *
import zipfile
from macholib.util import * 
from scanApp import *
from utils import *


#find the string in a file
def findString(fileName):
    privateApi = []
    frameworks = getFramework(fileName)
    fout = fileName.split("/")[-1]
    with open("privateApi","r") as inF:
        for line in inF:
            line = line.strip()
            newline = json.loads(line)
            framework = newline.get("framework","")
            class_ = newline.get("class","")
            method = newline.get("method","")
            if framework in frameworks:
                logger.info("this app may contains private api,and it needs further vetting")
                result = readSections(fileName,framework,class_,method)
                if result!=None:
                    privateApi.append(result)
                    
    if(len(privateApi)>0):
        s = "\t"
        for pa in privateApi:
            framework = pa.get("framework")
            class_ = pa.get("class_")
            method = pa.get("method")
            s = s + "framework:" + framework + "class:" + class_ + "method:" + method + "\n"
        s = s[:-1]
        f_handle = open("outputReport/" + fout + ".txt","a+")
        f_handle.write("this application contains " + str(len(privateApi)) + " private api as follows:")
        f_handle.write(s)
        f_handle.close() 
    else:
        logger.info("this app may contains no private api")

#extract the macho file from the ipa and save it in the machoFiles    
def extractMachoFile(path):
    filelist = readPath(path)
    logger.info("It is preparing extracting MachoFile from the sample")
    for filename in filelist:
        filename = path + "/" + filename
        myzip = ZipFile(filename)
        myfilelist = myzip.namelist()
        
        for name in myfilelist:
            names = name.split("/")
            f_out = "machoFiles/" + names[-1]
            if f_out == "machoFiles/":
                continue
            with open(f_out,"wb") as f:
                f.write(myzip.read(name))
            if is_platform_file(f_out):
                logger.info("the name of the macho file is " + f_out)
            elif names[-1]=="Info.plist" and names[-2].find(".app")!=-1:
                os.system("cp " + f_out + " InfoFiles/" + names[-2].split(".")[0] + "_" + name.split("/")[-1])
            else:
                os.remove(f_out)
        myzip.close()
        os.remove(filename)
        
def extractInfoFile(path):
    filelist = readPath(path)
    logger.info("It is preparing extracting Info.plist from the sample")
    for filename in filelist:
        filename = path + "/" + filename
        myzip = ZipFile(filename)
        myfilelist = myzip.namelist()
        
        for name in myfilelist:
            names = name.split("/")
            if names[-1]=="Info.plist" and names[-2].find(".app")!=-1:
                print(name)
                f_out = "InfoFiles/" + names[-2].split(".")[0] + "_" + name.split("/")[-1]
                with open(f_out,"wb") as f:
                    f.write(myzip.read(name))
   
#test method
def main(path):
    fileList = readPath(path)
    for f in fileList:
        findString(path + "/" + f)
        
if __name__ == "__main__":
    logger = setLogger()
#     path = "machoFiles/"
#     main(path)
#     extractMachoFile("sample/")
#     print(is_platform_file("machoFiles/locka"))
    frameworks = getFramework("machoFiles_iphone/YoukuiPhone WatchKit Extension")
    for s in frameworks:
        print(s)
#     for s in strings("machoFiles/locka"):
#         if s.find("MobileInstallation")!=-1:
#             print(s)

