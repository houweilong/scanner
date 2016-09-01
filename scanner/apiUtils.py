'''
Created on Nov 18, 2015

@author: hwl122902
'''
import os
import logging
import json

def setLogger():
    logger_root = logging.getLogger()
    console = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(process)d][%(filename)s]%(funcName)s: %(message)s")
    console.setFormatter(formatter)
    logger_root.addHandler(console)
    logger_root.setLevel(logging.INFO)
    return logger_root

def insert(frameworkName,className="",methodName=""):
    with open("privateApi","a+") as f:
        api = {}
        api["framework"] = frameworkName
        if className!="":
            api["class"] = className
        if methodName!="":
            api["method"] = methodName
        f.write("\n")
        f.write(str(api).replace("\'", "\""))
        logger.info("insert sucessful")
        
def delete(frameworkName,className="",methodName=""):
    f_old = open("privateApi","r").readlines()
    result = False
    
    for i in range(len(f_old)):
        line = f_old[i].strip()
        newline = json.loads(line)
        framework = newline.get("framework","")
        class_ = newline.get("class","")
        method = newline.get("method","")
        if frameworkName==framework and className==class_ and method==methodName:
            result = True
            logger.info(line)
        else:
            with open("newapi","a+") as f:
                f.write(line + "\n")
                
    f_new = open("newapi","r").readlines()
    for i in range(len(f_new)):
        with open("new","a+") as f:
            if i==len(f_new)-1:
                f.write(f_new[i].strip())
            else:
                f.write(f_new[i].strip() + "\n")
    os.remove("newapi")
                
    os.rename("new", "privateApi")
    if result==True:
        logger.info("delete sucessful")
        return True
    else:
        logger.info("delete fail")
        return False
        

def search(frameworkName,className="",methodName=""):
    f_old = open("privateApi","r").readlines()
    for line in f_old:
        line = line.strip()
        newline = json.loads(line)
        framework = newline.get("framework","")
        class_ = newline.get("class","")
        method = newline.get("method","")
        if frameworkName==framework and className==class_ and method==methodName:
            logger.info("search it sucessfully")
            return True
    logger.info("search it failly")
    return False
        
if __name__=="__main__":
    logger = setLogger()
#     f = insert("AdSupport", "ASIdentifierManager","advertisingTrackingEnabled")
#     insert("world")
    search("libsystem","ptrace")
