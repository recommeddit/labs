import requests, json, time, pandas as pd, re

"""
This parses reddit threads given a URL
"""
def parse_thread(url):
    print(url)
    json_tree = requests.get(url + '.json', headers = {'User-agent': 'testing 0.1'}).json()

    # Get simple data
    try:
        title = json_tree[0]['data']['children'][0]['data']['title']
        self_text = json_tree[0]['data']['children'][0]['data']['selftext']
        score = json_tree[0]['data']['children'][0]['data']['score']
        num_comments = json_tree[0]['data']['children'][0]['data']['num_comments']
    except:
        title, self_text, score, num_comments, comments = None, None, None, None, None
        return {'title':title, 'self_text':self_text, 'score':score,
                'num_comments':num_comments, 'comments':comments}

    # Get top level comments
    try:
        children = json_tree[1]['data']['children']
    except:
        comments = None
        return {'title':title, 'self_text':self_text, 'score':score,
                'num_comments':num_comments, 'comments':comments}

    comments = []
    for child in children:
        try:
            comments.append(child['data']['body'])
        except:
            print('failed: ', child)

    return {'title':title, 'self_text':self_text, 'score':score,
            'num_comments':num_comments, 'comments':comments}

"""
This parses google search results given a query
"""
def get_links(query):
    words = query.split(' ')
    if words[-1] != 'Reddit' or words[-1] != 'reddit':
        words.append('reddit')
    url = 'https://www.google.com/search?q=' + '+'.join(words)
    print('querying {0}'.format(' '.join(words)))  # Debug
    page = str(requests.get(url).content)
    links = re.finditer(r'https://www\.reddit\.com/r/[\w]+/comments/.*?/', page)
    for link in links:
        yield page[link.start():link.end()]

"""
This reads from a csv to generate lists of queries
"""
def get_queries(path):
    df = pd.read_csv(path, skiprows=[1])
    # return list(df.iloc[:1,0])  # DEBUG; REMOVE
    return (i for i in df.iloc[:,0])

def create_data(queries_path, save_path):
    def save():
        df = pd.DataFrame(threads, columns=['title', 'self_text', 'score',
                                            'num_comments', 'comments'])
        df.to_csv(save_path)

    queries = get_queries(queries_path)
    threads = []
    counter = 0
    for query in get_queries(queries_path):
        for link in get_links(query):
            print(f'parsing {link}')
            threads.append(parse_thread(link))
            counter += 1
            if counter % 10: save()

    # threads = []
    # for link in links:
    #     print('parsing {0}'.format(link))  # Debug
    #     threads.append(thread(link))


def generate_negative_queries(number):
    pass

def main():
    path = 'pos_queries.csv'
    save_to = 'pos_data.csv'
    create_data(path, save_to)

main()
