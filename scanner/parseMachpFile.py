'''
Created on Nov 18, 2015

@author: hwl122902
'''
from __future__ import print_function
from utils import *
import os
from macholib.util import fileview
from parsePlistFile import readInfoFile
import json

def readMachoFile(path):
    rout = {}
    logger.info("It is getting the header of the MachoFile")
    header = getHeader(path)
    descripe = dict(header.header._describe())
    cupType = descripe.get("cputype_string")
    rout["MachHeader"] = descripe
    commands = []
    logger.info("It is getting the contents of the MachoFile")
    for (index,(lc, cmd, data)) in enumerate(header.commands):
        
        lc_name = lc.get_cmd_name()
        if lc_name==44:
            if cupType.find("64")!=-1:
                lc_name = "LC_ENCRYPTION_INFO_64"
            else:
                lc_name = "LC_ENCRYPTION_INFO"
        desc = cmd.describe()
        
        if lc_name=="LC_SEGMENT_64" or lc_name == "LC_SEGMENT":
            sec_num = cmd.nsects
            if sec_num > 0:
                for sec in data:
                    secDesc = sec.describe()
                    strs = ''
                    with open(path, 'rb') as fp:
                        fh = fileview(fp, sec.addr, sec.size)
                        fh.seek(0)
                        with open("temp","wb") as f:
                            f.write(fh.read())
                         
                        for s in strings("temp"):
                            if isinstance(s, str):
                                strs = strs + s + ','
                         
                    secDesc["strings"] = strs
                    desc[str(sec.sectname.rstrip('\x00'))] = secDesc
                    os.remove("temp")
        else:
            desc["data"] = data.rstrip('\x00')
        commands.append(desc)
    rout["loadcommand"] = commands
    return rout
        
def outputResult(path):
    out = {}
    js_macho = readMachoFile(path)
    js_plist = readInfoFile("Info.plist")
    out["machoPart"] = js_macho
    out["plistPart"] = js_plist
    outFinal = json.dumps(out, encoding='latin1')
    with open("result","w") as f:
        f.write(outFinal)

if __name__ == "__main__":
    logger = setLogger()
    path = "machoFiles/IPadQQ"
    outputResult(path)


