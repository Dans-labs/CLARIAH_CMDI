# CMDI/XML exploration tool

by Slava Tykhonov, Data Archiving and Networked Services (DANS-KNAW) https://dans.knaw.nl

*This package created for CLARIAH+ WP3 https://clariah.nl

*Licensed under GPLv3*

# Usage

```
usage: cmdi2dict.py [-h] [-j] [-s] [-H] [-i inputfile] [-o outputfile] [-D inputfolder] 

optional arguments:
  -h, --help                  show this help message and exit
  -v, --verbose               verbose mode for debug messages
  -j, --json                  convert CMDI format to JSON
  -s, --stats                 generate statistics of CMDI fields
  -H, --hierarchy             extract hierarchy of CMDI fields 
  -i inputfile, --ifile       Input CMDI file
                              Provide an input file in CMDI/XML format
  -d inputfolder, --idir      Input folder with CMDI files
                              Does processing of all fields in the folder
  -o outputfile, --ofile      Output file 
                              Provide an file to save fields statistics or export metadata 
```

# Test data
Some CMDI examples available for testing purposes in /tests folder

# Collecting statistics of CMDI fields

```
cmdi2dict.py -s -i ./tests/test2.xml
```
Expected result is the frequency statistics of all fields
```
Title 160
Topic 80
Code 64
Country 16
Region 16
Address 16
Continent 16
Location 8
DOCMAP 4
#document 2
None
```

# Convert CMDI file to JSON
```
cmdi2dict.py -j -i ./tests/test2.xml
```
Expected result is JSON record
```
{'#document': {'DOCMAP': {'Topic': [{'#attributes': {'Target': 'ALL'}, 'Title': 'My Document'}, {'Topic': [{'#attributes': {'Target': 'ALL'}, 'Title': 'Basic Features'}, {'Topic': {'#attributes': {'Target': 'ALL'}, 'Title': 'Platforms Supported'}, '#attributes': {'Target': 'ALL'}, 'Title': 'About This Software'}], '#attributes': {'Target': 'ALL'}, 'Title': 'Overview'}], 'Location': {'Country': {'Code': 'NL'}, 'Region': 'Unknown', 'Continent': {'Code': 'EU'}, 'Address': 'often stated in the first part of the audio recording'}}}}
```

# Extract hierarchy from CMDI file(s)
```
cmdi2dict.py -H -i ./tests/test2.xml
```
Expected result is the list of the hierarchy of fields
```
	 /#document/DOCMAP/Topic/#attributes
	 /#document/DOCMAP/Topic/#attributes/Target
	 /#document/DOCMAP/Topic/Title
	 /#document/DOCMAP/Location
	 /#document/DOCMAP/Location/Country
	 /#document/DOCMAP/Location/Country/Code
	 /#document/DOCMAP/Location/Region
	 /#document/DOCMAP/Location/Continent
	 /#document/DOCMAP/Location/Continent/Code
	 /#document/DOCMAP/Location/Address
```

# Process all CMDI files in the selected folder and collect statistics
```
cmdi2dict.py -s -d ./tests
```
Expected result
```
Title 320
Topic 160
Code 64
Region 16
Country 16
Address 16
Continent 16
Location 8
DOCMAP 8
#document 4
```
