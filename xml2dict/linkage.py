import json
import requests
from skosmos_client import SkosmosClient, SkosmosConcept

class Draftlinkage():
    def __init__(self, sourceobject=None, content=None, debug=False):
        self.keywords = {}
        self.geoconcepts = {}
        self.source = sourceobject
        self.linkagesource = 'https://query.wikidata.org/sparql#entities-all'
        self.apiskosmos = 'http://api.finto.fi/rest/v1/'
        self.debug = 'True' #debug
        self.geosource = 'yso-paikat'

    def conceptmaker(self, cotype, q, s):
        if cotype == 'nde':
            return self.ndegrapql(q, s)
        if cotype == 'skosmos':
            return self.skosmosql(q, s)
        return

    def skosmosql(self, q, s):
        results = {}
        query = q + '*'
        skosmos = SkosmosClient(api_base=self.apiskosmos)
        results['rawdata'] = skosmos.search(query, vocabs=s, lang="en")
        print(len(results['rawdata']))
        concepturi = []
        for concept in results['rawdata']:
            if 'uri' in concept:
                payload = {'uri': concept['uri'], 'format': 'application/ld+json'}
                url = self.apiskosmos + s + '/data' 
                req = requests.get(url, params=payload)
                data = req.json()
                concepturi.append({ concept['uri']: data })

        results['uri'] = concepturi
        return results

    def ndegrapql(self, q, s):
        results = {}
        headers = {"content-type":"application/json"}
        query = "{\"query\":\"query Terms {  terms(sources: [\\\"" + s + "\\\"], query: \\\"" + q + "\\\") {    source {      uri      name      creators {        uri        name        alternateName      }    }    result {      __typename      ... on Terms {        terms {          uri          prefLabel          altLabel          hiddenLabel          scopeNote          broader {            uri            prefLabel          }          narrower {            uri            prefLabel          }          related {            uri            prefLabel          }        }      }      ... on Error {        message      }    }  }}\"}"
        r = requests.post("https://termennetwerk-api.netwerkdigitaalerfgoed.nl/graphql", data=query, headers=headers)
        results['rawdata'] = r.json()
        return results

    def linkage(self, x):
        if isinstance(x, list):
            return [self.linkage(v) for v in x]
        elif isinstance(x, dict):
            for k, v in x.items():
                if k == '1Keyword':
                    for keyword in v:
                        search = self.conceptmaker('nde', keyword, self.linkagesource)
                        if search:
                            if self.debug:
                                print("%s => %s\n" % (keyword, search))
                            self.keywords[keyword] = search
                if k == 'SpatialCoverage':
                    concepts = {}
                    skossearch = self.conceptmaker('skosmos', v, self.geosource)
                    if skossearch:
                        concepts['skosmos'] = skossearch
                    search = self.conceptmaker('nde', v, self.linkagesource)
                    if search:
                        concepts['nde'] = search
                        if self.debug:
                            print("%s => %s\n" % (v, search))
                    self.geoconcepts[v] = concepts
            return {k[0].upper() + k[1:]: self.linkage(v) for k, v in x.items()}
        else:
            return x
