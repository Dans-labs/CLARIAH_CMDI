# -*- coding: utf-8 -*-
# CMDI/XML convertion tool
# Created and maintained by Slava Tykhonov (DANS-KNAW)
import sys
#reload(sys)  
import os
import requests
#sys.setdefaultencoding('utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
from xml.dom import minidom
from xml2dict.processor import CMDI # load, xmldom2dict
from xml2dict.linkage import Draftlinkage
import getopt
import json

def usage():
    print("CMDI/XML convertion tool")
    print('Usage: cmdi2dict.py [parameters] -i <inputfile> ')
    print("Available parameters are:")
    print("\t-h show this usage")
    print("\t-v verbose mode for debug purposes")
    print("\t-s generate fields statistics")
    print("\t-S generate schema")
    print("\t-H extracti fields hierarchy")
    print("\t-j convertion to JSON format")
    print("\t-l start linking process")
    print("\t-i inputfile")
    print("\t-d inputfolder")
    print("\t-o outputfile")
    return

if __name__=='__main__':
    input = ''
    actions = {}
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hsvSHjli:o:d:",["ifile=","idir=","ofile="])
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
        elif opt == '-S':
           actions['schema'] = True
        elif opt == '-v':
           actions['verbose'] = True
        elif opt == '-j':
           actions['json'] = True
        elif opt == '-l':
           actions['linking'] = True
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
        cmdi = CMDI(actions)
        d = cmdi.load(input)
        
        if 'stats' in actions:
            print(cmdi.printstats())
        if 'json' in actions:
            jsonobj = json.dumps(cmdi.json)
            print(jsonobj)
        if 'hierarchy' in actions:
            print(cmdi.gethierarchy())
        if 'schema' in actions:
            print(cmdi.schema())
        if 'linking' in actions:
            jsonobj = json.dumps(cmdi.json)
            #d = linkage(cmdi.json)
            links = Draftlinkage(cmdi.json)
            links.linkage(cmdi.json)
            #print(json.dumps(d, indent=4, sort_keys=True)) 
            print(json.dumps(links.geoconcepts, indent=4, sort_keys=True))

    if os.path.isdir(input):
    # Show all CMDI files in folder
        cmdif = CMDI(actions)
        d = cmdif.loadfolder(input)
        for filename in cmdif.content:
            links = Draftlinkage(filename) #cmdif.content[filename])
            links.linkage(cmdif.content[filename])
            print(json.dumps(links.geoconcepts, indent=4, sort_keys=True))
        #print(json.dumps(cmdif.content, indent=4, sort_keys=True))
        #print(cmdif.printstats())
        #print(cmdif.schema())
        
 
