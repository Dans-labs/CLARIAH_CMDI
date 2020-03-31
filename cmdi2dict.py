# -*- coding: utf-8 -*-
import sys
reload(sys)  
import os
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
from xml.dom import minidom
from xml2dict.processor import load, xmldom2dict

if __name__=='__main__':
    #data = minidom.parse(sys.argv[1])
    #d=xmldom2dict(data)
    d = load(sys.argv[1])
    print(d)
