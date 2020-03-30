# -*- coding: utf-8 -*-
import sys
reload(sys)  
sys.setdefaultencoding('utf-8')
from xml.dom import minidom
from xml2dict import xmldom2dict

if __name__=='__main__':
    data = minidom.parse(sys.argv[1])

    d=xmldom2dict(data)

    print d
