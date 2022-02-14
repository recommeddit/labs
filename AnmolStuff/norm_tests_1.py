#!/usr/bin/env python3

import requests
import urllib.parse
from pprint import pprint

params = {
    "action" : "query",
    "format" : "json",
    "prop" : "info",
    "list" : "search",
    "srsearch" : "wikipedia",
    "srlimit" : 3,
    "srprop" : "sectiontitle"
}

print("Press Ctrl-C / Cmd-C to exit this demo...")
try:
    while True:
        params["srsearch"] = input("Search Wikipedia: ")
        for r in requests.get('https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode(params, doseq=True)).json()['query']['search']:
            print('title ==>', r['title'])
            print('\tns ==>', r['ns'])
            print('\tpage id ==>', r['pageid'])
            print('\turl ==> https://en.wikipedia.org/wiki?curid=' + str(r['pageid']))
except KeyboardInterrupt:
    print("Thank you for using this demo!")
