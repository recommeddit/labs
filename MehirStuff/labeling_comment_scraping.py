import requests, pandas as pd, re

"""
This reads from a csv to generate lists of queries
"""
def get_queries(path):
    df = pd.read_csv(path, skiprows=[1])
    # return list(df.iloc[:1,0])  # DEBUG; REMOVE
    return (i for i in df.iloc[:20,1])

"""
This parses google search results given a query
"""
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

"""
These two functions parse a whole thread for comments only
"""
def recursive_parse_comments(json_tree):
    comments = []
    for child in json_tree:
        try:
            comments.append(child['data']['body'])
            try:
                comments.extend(recursive_parse_comments(
                            child['data']['replies']['data']['children']))
            except:
                pass
        except:
            pass
    return comments

def parse_comments_step_1(url):
    json_tree = requests.get(url + '.json', headers = {'User-agent': 'testing 0.1'}).json()
    comments = []
    try:
        children = json_tree[1]['data']['children']
        for child in children:
            try:
                comments.append(child['data']['body'])
                try:
                    comments.extend(recursive_parse_comments(
                                child['data']['replies']['data']['children']))
                except:
                    pass
            except:
                print('failed: ', child)
    finally:
        return comments

"""
This creates the data
"""
def create_data(queries_path, save_path):
    queries = get_queries(queries_path)
    all_comments = []
    counter = 0
    for query in get_queries(queries_path):
        for link in get_links(query):
            print(f'parsing {link}')
            all_comments.extend(parse_comments_step_1(link))

    df = pd.DataFrame(all_comments)
    df.to_csv(save_path)

"""
Main method
"""
def main():
    create_data('pos_data.csv', 'comments.csv')

main()
