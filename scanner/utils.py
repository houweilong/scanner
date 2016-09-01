'''
Created on Dec 16, 2015

@author: hwl122902
'''

from __future__ import print_function
import string
import logging
import os
from macholib.MachO import MachOHeader
from macholib.MachO import MachO

def setLogger():
    logger_root = logging.getLogger()
    console = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(process)d][%(filename)s]%(funcName)s: %(message)s")
    console.setFormatter(formatter)
    logger_root.addHandler(console)
    logger_root.setLevel(logging.INFO)
    return logger_root

def getHeader(path):
    m = MachO(path)
    for header in m.headers:
        if isinstance(header, MachOHeader):
            return header
    return None

def strings(filename, min=4):
    with open(filename, "rb") as f:
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                yield result
            result = ""

def getFramework(filename):
    header = getHeader(filename)
    seen = set()
    #for all relocatable commands,yield (command_index, command_name, filename)
    for idx, name, other in header.walkRelocatables():
#         if other.find("framework")!=-1:
#             others = other.split("/")
#             fw = others[-1]
        if other not in seen:
            seen.add(other)
    return seen

#return all the file in this path
def readPath(path):
    fileList = []
    files = os.listdir(path)
    for f in files:
        if(os.path.isfile(path + "/" + f)):
            fileList.append(f)
    return fileList