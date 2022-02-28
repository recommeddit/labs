#!/usr/bin/env python3

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
        processed_results : type = bool, True if queried results provide reputable answers
                                         False if not
    WARNING: limited queries (100 - 10000)
    """
    configuration = config() # pulls data from project.ini file

    if "apikey" not in configuration.keys():
        raise KeyError("Please provide an apikey in an initialization file. Contact Anmol for more info.")

    params = {
        "q" : query_string.lower(),
        "api_key" : configuration["apikey"]
    }

    search = GoogleSearch(params) # complete Google search with params

    del configuration, params # delete the configuration dictionaries that hold the api key

    results = search.get_dict()
    return process_results(query_string, results) # check if results are good

def process_results(query_string, results):
    """
    Process the results from the google search query to determine if the queried
    recommendation candidate is acceptable.

    This implementation of process_results checks to see if all query terms are
    included in the web result. This does not consider knowledge graph results.

    input:
        query_string : type = str, the google search query which provided results
        results : type = dict, the results of the Google Search
    output:
        boolean : True if this candidate is acceptable and exists
                  False if not
        link    : type = str, the search result that trusts this candidate
    """
    words = query_string.split(' ')
    for web_result in results['organic_results']:
        count = 0
        for word in words:
            if word in ' '.join(web_result['about_this_result']['keywords']).lower() or word in web_result['title'].lower() or word in web_result['snippet'].lower():
                count += 1
        if count == len(words):
            print(web_result['link'])
            return (True, web_result['link'])
    return (False, None)

def clean_string(s):
    """
    Clean the string (ie, remove all common punctuation characters)

    input:
        s : type = str, the string that needs to be cleaned
    output:
        str : the processed string
    """
    s = re.sub('["!#$%*]', '', s) # remove bad chars
    return s

def gkg_query(query_string, threshold=1, print_results=False):
    """
    Use Google's Knowledge Graph Search API call and analyze the results to check
    if the output is reasonable for our search query

    input:
        query_string : type = str, some google search query you want
        threshold : type = int, accept all query results which have do not have these
                    many words in their detailed description from the query string,
                    default = 1 -- only one missing word will be tolerated
    """
    configuration = config(section='kgsearch') # get config data from project.ini

    if "api_key" not in configuration.keys():
        raise KeyError("Please provide an apikey in an initialization file. Contact Anmol for more info.")

    params = {
        'query' : query_string,
        'limit' : 10,
        'indent' : True,
        'key' : configuration['api_key']
    }

    # query KG
    url = 'https://kgsearch.googleapis.com/v1/entities:search' + '?' + urllib.parse.urlencode(params)
    if print_results:
        print(url, end="\n\n")
    response = json.loads(urllib.request.urlopen(url).read())

    # process results
    query_string = clean_string(query_string)
    if print_results:
        print(response)
    for result in response['itemListElement']:
        if result['resultScore'] < 1:
            continue
        word_count = 0
        for word in query_string.split():
            try:
                if word.lower() in clean_string(result['result']['detailedDescription']['articleBody'].lower()).split():
                    word_count += 1
                    continue
            except:
                return (False, None)
        if word_count >= len(query_string.split()) - threshold:
            if print_results:
                print(f"Query of `{query_string}` found TRUE by the following search result:\n")
                print(result)
            return (True, )
    return (False, None)

if __name__ == '__main__':
    query_string = 'vscode ide'
    print('Query:', query_string, end='\n\n\n\n')

    res1 = gkg_query(query_string, threshold=1, print_results=True)
    res2 = False #with_serp(query_string)
    if res1:
        print("SUCCESS 1")
    elif res2[0]:
        print("SUCCESS 2")
    else:
        print("FAILURE")
