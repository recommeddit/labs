#!/user/bin/env python3

from __future__ import print_function
from serpapi import GoogleSearch
from config import config
import json, urllib, re

def with_serp(query_string):
    """
    with_serp uses the Serp API to provide Google Search results
    The API key is pulled using the config() method from config.py
    Additional help information can be found on `https://serpapi.com/`
    input:
        query_string : type = str, some google search query you want
    output:
        proccessed_results : type = bool, True if queried results provide reputable answers
                                         False if not
    """
    configuration = config()
    params = {
        "q" : query_string,
        "api_key" : configuration["apikey"]
    }

    search = GoogleSearch(params)

    del configuration, params # delete the configuration dictionaries that hold the api key

    results = search.get_dict()
    return process_results(query_string, results)

def process_results(query_string, results):
    """
    Process the results from the google search query to determine if the queried
    recommendation candidate is acceptable.

    Currently, this implementation of process_results only checks if a knowledge
    graph result exists or not.

    input:
        query_string : type = str, the google search query which provided results
        results : type = dict, the results of the Google Search
    output:
        boolean : True if this candidate is acceptable and exists
                  False if not
    """
    if "knowledge_graph" in results:
        return True
    return False

def clean_string(s):
    """
    Clean the string (ie, remove all common punctuation characters)

    input:
        s : type = str, the string that needs to be cleaned
    output:
        str : the processed string
    """
    s = re.sub('["!#$%*]', '', query_string)
    return s

def gkg_query(query_string, threshold=1):
    """
    Use Google's Knowledge Graph Search API call and analyze the results to check
    if the output is reasonable for our search query

    input:
        query_string : type = str, some google search query you want
        threshold : type = int, accept all query results which have do not have these
                    many words in their detailed description from the query string,
                    default = 1 -- only one missing word will be tolerated
    """
    configuration = config(section='kgsearch')

    params = {
        'query' : query_string,
        'limit' : 10,
        'indent' : True,
        'key' : configuration['api_key']
    }

    url = 'https://kgsearch.googleapis.com/v1/entities:search' + '?' + urllib.parse.urlencode(params)
    response = json.loads(urllib.request.urlopen(url).read())
    query_string = clean_string(query_string)
    print('Query:', query_string, end='\n\n\n\n')
    for result in response['itemListElement']:
        if result['resultScore'] < 1:
            continue
        word_count = len(query_string)
        for word in query_string:
            if word.lower() in clean_string(result['result']['detailedDescription']['articleBody'].lower()).split():
                word_count += 1
        if word_count == len(query_string) - threshold:
            return True
    return False

if __name__ == '__main__':
    gkg_query('"PyCharm" Java IDE')
