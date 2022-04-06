#!/usr/bin/python3

import requests, re
import urllib.parse
import time

pattern_cat = re.compile('<div class="wikibase-entitytermsview-heading-description ">(.+?)</div>')
pattern_tit = re.compile('<title>(.+?)</title>')

params = {
    "action" : "query",
    "format" : "json",
    "prop" : "categories|categoryinfo|description|duplicatefiles|entityterms|extlinks|extracts|fileusage|globalusage|imageinfo|images|info|iwlinks|langlinks|links|linkshere|mapdata|mmcontent|pageimages|pageprops|pageterms|redirects|pageviews|revisions|templates|transcludedin|videoinfo",
    "list" : "search",
    "srsearch" : "wikipedia",
    "srlimit" : 3,
    "srprop" : "sectiontitle"
}

__sources__ = ['wikipedia']

def top_wiki(query, n=3):
    '''
    Return the top n results when searching for possible normalized versions of
    the query using the Wikipedia API
    Input:
        - query : type == str, string to be deduped
        - n : the maximum number of possible normalized strings you want
    Output:
        - array, length n, contains only the title of the wikipedia article
    '''
    params['srlimit'] = n
    params['srsearch'] = query.lower()
    results = requests.get('https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode(params, doseq=True)).json()['query']['search']

    return [r['title'] for r in results]

def top_wikidata(query, n=3):
    '''
    Return the top n results when searching for possible normalized versions of
    the query using the Wikipedia API
    Input:
        - query : type == str, string to be deduped
        - n : the maximum number of possible normalized strings you want
    Output:
        - array, length n, contains only the title of the wikipedia article
    '''
    params['srlimit'] = n
    params['srsearch'] = query.lower()
    results = requests.get('https://wikidata.org/w/api.php?' + urllib.parse.urlencode(params, doseq=True)).json()['query']['search']

    return [r['title'] for r in results]

def wikidata(link):
    link = f"https://www.wikidata.org/wiki/{link}"
    data = requests.get(link).text
    return [re.findall(pattern_tit, data)[0].split(" - Wikidata")[0], re.findall(pattern_cat, data)[0]]

if __name__ == '__main__':
    # test out wikidata api
    q = "syntax.fm"
    t1 = time.time()
    res1 = top_wikidata(q, n=5)
    print("Wikidata", res1)
    for f in res1:
        print(wikidata(f))

    # test out wikipedia api
    t2 = time.time()
    print("Wikipedia", top_wiki(q, n=5))
    t3 = time.time()

    # print out the times of the tests
    print("Wikipedia", t3-t2)
    print("Wikidata", t2-t1, 'sec')
