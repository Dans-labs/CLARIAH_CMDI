# -*- coding: utf-8 -*-
import sys
reload(sys)  
import os
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
from xml.dom import minidom
from xml2dict.processor import CMDI # load, xmldom2dict

if __name__=='__main__':
    cmdi = CMDI()
    d = cmdi.load(sys.argv[1])
    print(d)
