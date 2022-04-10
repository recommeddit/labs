#!/usr/bin/env python3

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

    if 'knowledge_graph' in results.keys():
        if 'description' in results['knowledge_graph'].keys():
            count = 0
            for word in words:
                if word in result['knowledge_graph']['title'] or word in result['knowledge_graph']['description'].lower():
                    count += 1
            if count == len(words):
                src = results['knowledge_graph']['source']['link']
                if 'header_images' in results['knowledge_graph'].keys():
                    return (True, [src, results['knowledge_graph']['header_images']['image']])
                elif 'image' in results['knowledge_graph'].keys():
                    return (True, [src, results['knowledge_graph']['image']])

    for web_result in results['organic_results']:
        count = 0
        for word in words:
            if word in ' '.join(web_result['about_this_result']['keywords']).lower() or word in web_result['title'].lower() or word in web_result['snippet'].lower():
                count += 1
        if count == len(words):
            img = ''
            if 'thumbnail' in web_result.keys():
                img = web_result['thumbnail']
            return (True, [web_result['link'], img])
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
    response = json.loads(urllib.request.urlopen(url).read())

    # process results
    query_string = clean_string(query_string)
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
            urls = []
            if 'url' in result['result']['detailedDescription'].keys():
                urls.append(result['result']['detailedDescription']['url'])
            else:
                urls.append('')
            if 'image' in result['result'].keys() and 'contentUrl' in result['result']['image'].keys():
                urls.append(result['result']['image']['contentUrl'])
            else:
                urls.append('')
            return (True, urls)
    return (False, None)

def search(query_string):
    try:
        results = gkg_query(query_string)
        if not results[0]:
            results = with_serp(query_string)
            if not results[0]:
                return (False, ['',''])
            else:
                return results
        else:
            return results
    except:
        return (False, ['',''])

if __name__ == '__main__':
    print(search('visual studio ide'))
