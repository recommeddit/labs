import requests, pandas as pd, re, html

def get_queries(path):
    df = pd.read_csv(path, skiprows=[1])
    # return list(df.iloc[:1,0])  # DEBUG; REMOVE
    return (i for i in df.iloc[:,0])

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

def main():
    queries_path = 'pos_queries.csv'
    queries = get_queries(queries_path)
    pages = []
    for query in get_queries(queries_path):
        for link in get_links(query):
            print(f'loading {link}')
            pages.append(get_page(link))

    print(pages)

main()
