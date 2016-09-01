'''
Created on Dec 9, 2015

@author: hwl122902
'''
from biplist import *
from utils import *

def readInfoFile(path):
    logger = setLogger()
    try:
        logger.info("It is preparing parsing Info.plist")
        fout = {}
        plist = readPlist(path)
        fout["plist"] = plist
        logger.info("It has finished parsing Info.plist")
        return fout
    except (InvalidPlistException, NotBinaryPlistException), e:
        print("this file is not a plist:", e)
        
if __name__ == "__main__":
    path = "InfoFiles/IPadQQ_Info.plist"
    readInfoFile(path)
