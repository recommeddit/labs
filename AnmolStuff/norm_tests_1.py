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
for i in range(10):
    params["srsearch"] = input("Search Wikipedia: ")
    pprint(requests.get('https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode(params, doseq=True)).json())
