# CLARIAHplus CMDI convertor
Usage: 
```
python ./cmdi2dict.py somefile.xml
```
Example:
```
python ./cmdi2dict.py ./tests/test2.xml 
```
Output:
```
{'#document': {'DOCMAP': {'Topic': [{'#attributes': {'Target': 'ALL'}, 'Title': 'My Document'}, {'Topic': [{'#attributes': {'Target': 'ALL'}, 'Title': 'Basic Features'}, {'Topic': {'#attributes': {'Target': 'ALL'}, 'Title': 'Platforms Supported'}, '#attributes': {'Target': 'ALL'}, 'Title': 'About This Software'}], '#attributes': {'Target': 'ALL'}, 'Title': 'Overview'}], 'Location': {'Country': {'Code': 'NL'}, 'Region': 'Unknown', 'Continent': {'Code': 'EU'}, 'Address': 'often stated in the first part of the audio recording'}}}}
```
