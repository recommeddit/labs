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

def matching(wd_ids, ents):
    # [[q1,q2,q3],[q2,a7,q5],[q5,q8,q9]]
    de_ind = [-1 for i in range(len(wd_ids))]
    for idx in range(len(wd_ids)):
        if de_ind[idx] != -1:
            continue
        int_list = [list(set(wd_ids[idx]).intersection(wd_ids[i])) if i != idx else [] for i in range(len(wd_ids))]
        print(int_list)
        cmp_len = [len(i) for i in int_list]
        max_cmp = max(cmp_len)
        if max_cmp == 0:
            de_ind[idx] = ents[idx]
        else:
            # there is a similar solution found by the deduplication process
            max_idx = cmp_len.index(max_cmp)
            # if de_ind[max_idx] != -1:
            #     de_ind[idx] = ents[idx]
            #     continue # this item has already been deduped
            print(idx, max_idx)
            index, max_index = min(idx,max_idx), max(idx,max_idx)
            if de_ind[index] != -1:
                de_ind[max_index] = ents[index]
            else:
                de_ind[index] = ents[index]
                de_ind[max_index] = ents[index]
    return de_ind

'''if __name__ == '__main__':
    print([['q1','q2','q3'],['q2','q7','q5'],['q5','q8','q9']])
    print(matching([['q1','q2','q3'],['q2','q7','q5'],['q5','q8','q9']], ['Output 1','Output 2','Output 3']))'''

if __name__ == '__main__':
    # test out wikidata api
    q1 = "vscode"
    q2 = "VS Code"
    q3 = "Visual Studio Code"
    q4 = "IDE"
    q5 = "Microsoft"
    t1 = time.time()
    res1 = top_wikidata(q1, n=5)
    res2 = top_wikidata(q2, n=5)
    res3 = top_wikidata(q3, n=5)
    res4 = top_wikidata(q4, n=5)
    res5 = top_wikidata(q5, n=5)
    results = [res1,res2,res3,res4,res5]
    entities = [q1,q2,q3,q4,q5]
    for i in range(len(results)):
        print(f"Res{i}:", results[i])
    print(matching(results, entities))

    # test out wikipedia api
    # print("Wikipedia", top_wiki(q, n=5))
    # t3 = time.time()
    #
    # # print out the times of the tests
    # print("Wikipedia", t3-t2)
    t2 = time.time()
    print("Wikidata", t2-t1, 'sec')
