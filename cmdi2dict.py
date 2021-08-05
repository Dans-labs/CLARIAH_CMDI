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
import getopt
import json
headers = {"content-type":"application/json"}

def ndegrapql(q, s):
    query = "{\"query\":\"query Terms {  terms(sources: [\\\"" + s + "\\\"], query: \\\"" + q + "\\\") {    source {      uri      name      creators {        uri        name        alternateName      }    }    result {      __typename      ... on Terms {        terms {          uri          prefLabel          altLabel          hiddenLabel          scopeNote          broader {            uri            prefLabel          }          narrower {            uri            prefLabel          }          related {            uri            prefLabel          }        }      }      ... on Error {        message      }    }  }}\"}" 
    r = requests.post("https://termennetwerk-api.netwerkdigitaalerfgoed.nl/graphql", data=query, headers=headers)
    return r.json()

def linkage(x):
   source = 'https://query.wikidata.org/sparql#entities-all'
   if isinstance(x, list):
     return [linkage(v) for v in x]
   elif isinstance(x, dict):
     for k, v in x.items():     
         if k == 'Keyword':
             for keyword in v:
                 search = ndegrapql(keyword, source)
                 if search:
                     print("%s => %s\n" % (keyword, search))
         if k == 'SpatialCoverage':
            search = ndegrapql(v, source)
            if search:
                 print("%s => %s\n" % (v, search))
     return {k[0].upper() + k[1:]: linkage(v) for k, v in x.items()}
   else:
     return x

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
            d = linkage(cmdi.json)
            print(json.dumps(d, indent=4, sort_keys=True)) 

    if os.path.isdir(input):
    # Show all CMDI files in folder
        cmdif = CMDI(actions)
        d = cmdif.loadfolder(input)
        #print(cmdif.printstats())
        print(cmdif.schema())
        
 
