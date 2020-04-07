# -*- coding: utf-8 -*-
# CMDI/XML convertion tool
# Created and maintained by Slava Tykhonov (DANS-KNAW)
import sys
reload(sys)  
import os
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
from xml.dom import minidom
from xml2dict.processor import CMDI # load, xmldom2dict
import getopt

def usage():
    print("CMDI/XML convertion tool")
    print('Usage: cmdi2dict.py -i <inputfile> -o <outputfile>')
    print("\t-h show this usage")
    print("\t-s generate fields statistics")
    print("\t-H extracti fields hierarchy")
    print("\t-j convertion to JSON format")
    return

if __name__=='__main__':
    input = ''
    actions = {}
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hsHji:o:d:",["ifile=","idir=","ofile="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
           usage()
           sys.exit()
        elif opt == '-s':
           actions['stats'] = True
        elif opt == '-H':
           actions['hierarchy'] = True
        elif opt == '-j':
           actions['json'] = True
        elif opt in ("-i", "--ifile"):
           input = arg
        elif opt in ("-o", "--ofile"):
           output = arg
        elif opt in ("-d", "--idir"):
           input = arg

    # Show usage message if there are no parameters
    if not input:
        usage()

    # Do processing of one CMDI file
    if os.path.isfile(input):
        cmdi = CMDI()
        d = cmdi.load(input)
        
        if 'stats' in actions:
            print(cmdi.printstats())
        if 'json' in actions:
            print(cmdi.json)
        if 'hierarchy' in actions:
            print(cmdi.gethierarchy())

    if os.path.isdir(input):
    # Show all CMDI files in folder
        cmdif = CMDI()
        d = cmdif.loadfolder(input)
        print(cmdif.printstats())
        
 
