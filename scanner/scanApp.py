'''
Created on Nov 18, 2015

@author: hwl122902
'''
from __future__ import print_function
import os
from macholib.util import fileview
from utils import *


def readSections(path,framework,class_="",method=""):
    methodNames = []
    classNames = []
    header = getHeader(path)
    for (index,(lc, cmd, data)) in enumerate(header.commands):
        lc_name = lc.get_cmd_name()
        
        if lc_name=="LC_SEGMENT_64" or lc_name == "LC_SEGMENT":
            sec_num = cmd.nsects
            if sec_num > 0:
                for sec in data:
                    sname = sec.sectname.rstrip('\x00')
                    if sname == "__objc_methname":
                        methodNames = readPartOfFiles(path,sec.offset, sec.size)
                    if sname == "__objc_classname":
                        classNames = readPartOfFiles(path,sec.offset, sec.size)
    for s in classNames:
        if s!=class_:
            continue
        else:
            for s1 in methodNames:
                if s1 == method:
                    result = {}
                    result["framework"] = framework
                    result["class_"] = class_
                    result["method"] = method
                    return result
    return None


def readPartOfFiles(path,offset,size):
    strs = []
    with open(path, 'rb') as fp:
        fh = fileview(fp, offset, size)
        fh.seek(0)
        with open("temp","wb") as f:
            f.write(fh.read())
#                          
        for s in strings("temp"):
            if isinstance(s, str):
                strs.append(s)
    os.remove("temp")
    return strs




if __name__ == "__main__":
    outPath = "outputReport/"
    logger = setLogger()
    path = "machoFiles/IPadQQ"
    readSections(path)


