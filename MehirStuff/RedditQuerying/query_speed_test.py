import requests, pandas as pd, re, html

def get_queries(path):
    df = pd.read_csv(path, skiprows=[1])
    # return list(df.iloc[:1,0])  # DEBUG; REMOVE
    return (i for i in df.iloc[:20,0])

def get_links(query):
    print(query)
    words = query.split(' ')
    if words[-1] != 'Reddit' or words[-1] != 'reddit':
        words.append('reddit')
    url = 'https://www.google.com/search?q=' + '+'.join(words)
    print('querying {0}'.format(' '.join(words)))  # Debug
    page = str(requests.get(url).content)
    links = re.finditer(r'https://www\.reddit\.com/r/[\w]+/comments/.*?/', page)
    for link in links:
        yield page[link.start():link.end()]

def get_page(url):
    try:
        return requests.get(url + '.json', headers = {'User-agent': 'testing 0.1'})
    except:
        return

def main1():
    queries_path = 'pos_queries.csv'
    queries = get_queries(queries_path)
    pages = []
    for query in get_queries(queries_path):
        for link in get_links(query):
            print(f'loading {link}')
            pages.append(get_page(link))

    print(pages)

"""
Custom bash thing
"""
def make_urls():
    tags = ["hl1rd3e", "hl32g5z", "hl2c2z0", "hl1zytq", "hl1m8q5", "hl3eplg", "hl29st1", "hl1aswf", "hl1v85z", "hl1ge6y", "hl1nuoq"]
    pages = []
    for tag in tags:
        print(f'fetching {tag}')
        url = 'https://www.reddit.com/r/AskReddit/comments/qw1ahi/all_the_countries_of_the_world_are_at_a_party/{0}.json'.format(tag)
        pages.append(requests.get(url, headers = {'User-agent': 'testing 0.1'}).content)
    # print(pages)
    print(len(tags))

def main():
    make_urls()

main()
