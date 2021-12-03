import requests, time, concurrent.futures, pandas as pd, re, html

"""
Global Variables
"""
URLS = ["https://www.reddit.com/r/movies/comments/2isv8p/what_are_some_good_mindfuck_movies_like_inception/",
        "https://www.reddit.com/r/MovieSuggestions/comments/n5w7p3/movies_similar_to_inception/",
        "https://www.reddit.com/r/NetflixBestOf/comments/8l7g9t/request_mindmelting_movies_similar_to_inception/",
        "https://www.reddit.com/r/movies/comments/cbxpnj/movies_like_interstellar_inception_and_arrival/",
        "https://www.reddit.com/r/movies/comments/g4jrx8/movie_recommendations_similar_to_ex_machina/",
        "https://www.reddit.com/r/AskReddit/comments/4gib6l/what_are_some_mindfuck_movies_like_shutter_island/",
        "https://www.reddit.com/r/booksuggestions/comments/k7x6xv/recommend_a_book_like_movies_inception/",
        "https://www.reddit.com/r/movies/comments/e3kndv/looking_for_great_movies_with_great_music_like/",
        "https://www.reddit.com/r/movies/comments/evryo/inception_picks_up_where_shutter_island_left_off/",
        "https://www.reddit.com/r/movies/comments/1ukv5u/looking_for_some_movies_similar_to_inception/"]
OUTPUT_FILE = 'output.csv'
HEADER = {'User-agent': 'Reccomeddit-Bot 0.101'}


"""
Uses regex to parse comments from requests object
"""
def parse_comments(request_object):
    text = request_object.text
    comments = re.findall(r'"body": "(.*?)"', text) # todo: preprocess these things a bit
    return [html.unescape(comment) for comment in comments]

"""
Uses json parser to get title, text, score, and number of comments from thread,
in that order. Returns None if fails to extract any attribute.
"""
def get_basic_info(request_object):
    json_tree = request_object.json()
    try:
        title = json_tree[0]['data']['children'][0]['data']['title']
        self_text = json_tree[0]['data']['children'][0]['data']['selftext']
        score = json_tree[0]['data']['children'][0]['data']['score']
        num_comments = json_tree[0]['data']['children'][0]['data']['num_comments']
    except:
        return None
    return [title, self_text, score, num_comments]

"""
Calls get_basic_info and parse_comments. Assembles their results into a list
of lists of the form [[title, text, score, num comments, comment] x N].
"""
def assemble_thread_info(url):
    global HEADER
    try:
        json_tree = requests.get(url + '.json?limit=200', headers=HEADER)
    except:
        print('caught a bad url')
        return None
    row_part_1 = get_basic_info(json_tree)
    if row_part_1 is None:
        return None
    row_part_2 = parse_comments(json_tree)
    if row_part_2 is None:
        row_part_1.append([])
        return row_part_1
    rows = []
    for row in row_part_2:
        rows.append(row_part_1 + [row])
    return rows

"""
Creates a thread to all assemble_thread_info for each URL passed to it.
"""
def thread_builder(urls):
    list_of_rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as exec:
        futures = [exec.submit(assemble_thread_info, url) for url in urls]
        for future in futures:
            result = future.result()
            if result is not None:
                list_of_rows.extend(result)
    return list_of_rows

"""
Main method. Creates dataframe and stores it to output file.
"""
def main():
    global URLS
    global OUTPUT_FILE
    rows = thread_builder(URLS)
    print(f'parsed {len(rows)} comments in ', end='')  # Debug
    df = pd.DataFrame(rows, columns=[
        'title', 'text', 'score', 'num comments', 'comment'])
    df.to_csv(OUTPUT_FILE)

"""
Prints time taken and comments parsed to stdout.
"""
if __name__ == '__main__':
    start = time.time()  # Debug
    main()
    end = time.time()  # Debug
    print(f'{end-start} seconds')  # Debug
