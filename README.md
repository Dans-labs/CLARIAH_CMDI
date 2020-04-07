============================
CMDI/XML exploration tool
============================

*by Slava Tykhonov, Data Archiving and Networked Services (DANS-KNAW) https://dans.knaw.nl

*Created for CLARIAH+ WP3

*Licensed under GPLv3*

# Usage

```
usage: cmdi2dict.py [-h] [-v] [-u URL] [-p PARAMS] [-H HEADER] [-a AGENT]
                   [-t THREADS] [-off VARIANCE] [-diff DIFFERENCE] [-o OUT]
                   [-P PROXY] [-x IGNORE] [-s SIZEIGNORE] [-d DATA]
                   [-i IGMETH] [-c COOKIE] [-T TIMEOUT]

optional arguments:
  -h, --help             show this help message and exit
  -j, --json             convert CMDI to JSON
  -s, --stats            generate statistics of CMDI fields
  -H, --hierarchy        extract hierarchy of CMDI fields 
  -i inputfile, --ifile  Input CMDI file
                         Provide an input file in CMDI/XML format
  -D inputfolder, --idir Input folder with CMDI files
                         Does processing of all fields in the folder
  -o outputfile, --ofile Output file 
                         Provide an file to save statistics or for export 
```

```
Output:
```
{'#document': {'DOCMAP': {'Topic': [{'#attributes': {'Target': 'ALL'}, 'Title': 'My Document'}, {'Topic': [{'#attributes': {'Target': 'ALL'}, 'Title': 'Basic Features'}, {'Topic': {'#attributes': {'Target': 'ALL'}, 'Title': 'Platforms Supported'}, '#attributes': {'Target': 'ALL'}, 'Title': 'About This Software'}], '#attributes': {'Target': 'ALL'}, 'Title': 'Overview'}], 'Location': {'Country': {'Code': 'NL'}, 'Region': 'Unknown', 'Continent': {'Code': 'EU'}, 'Address': 'often stated in the first part of the audio recording'}}}}
```
