'''
Created on Nov 18, 2015

@author: hwl122902
'''
from __future__ import print_function
from utils import *
import os
from macholib.mach_o import *
from macholib.util import fileview
from parsePlistFile import readInfoFile
import json

def readMachoFile(path):
    logger.info("It is getting the header of the MachoFile")
    header = getHeader(path)
    descripe = dict(header.header._describe())
    cupType = descripe.get("cputype_string")
    logger.info("It is getting the contents of the MachoFile")
    for (index,(lc, cmd, data)) in enumerate(header.commands):
        
        lc_name = lc.get_cmd_name()
        if lc_name==44:
            if cupType.find("64")!=-1:
                lc_name = "LC_ENCRYPTION_INFO_64"
            else:
                lc_name = "LC_ENCRYPTION_INFO"
        if lc_name=="LC_SEGMENT_64" or lc_name == "LC_SEGMENT":
            
            if cmd.segname.rstrip('\x00')=="__DATA":
                sec_num = cmd.nsects
                if sec_num > 0:
                    for sec in data:
                        if sec.sectname.rstrip('\x00') == "__const":
                            print(sec.addr)
                            print(sec.size)
                            print(sec.offset)
                            with open(path, 'rb') as fp:
                                fh = fileview(fp, sec.addr, sec.size)
                                fh.seek(0)
                                with open("temp","wb") as f:
                                    f.write(fh.read())
                                
                                for s in strings("temp"):
                                    if s.find("MobileInstallation")!=-1:
                                        print(s)
            
                                os.remove("temp")
                         
        

if __name__ == "__main__":
    logger = setLogger()
    path = "machoFiles/locka"
    readMachoFile(path)

