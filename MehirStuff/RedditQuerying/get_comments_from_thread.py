import requests, time, concurrent.futures, pandas as pd, re, html

"""
Uses regex to parse comments from requests object
"""
def parse_info(request_object):
    text = request_object.text
    comments = re.findall(r'"body": "(.*?)"', text)  # todo: preprocess comments
    if len(comments) == 0:  # If no comments, nothing to do
        return None
    scores = re.findall(r'"score":(.*?),', text)[1:]  # Ignore: first score is score of the thread
    links = re.findall(r'"permalink": "(.*?)",', text)[1:]  # Ignore: see above
    if not len(comments) == len(scores) == len(links):
        raise Exception('Unexpected thread format: link = {0}'.format(request_object.url))
    return [{'text':html.unescape(c), 'score':s, 'link':l} for c, s, l in zip(comments, scores, links)]

"""
Calls get_basic_info and parse_comments. Assembles their results into a list
of lists of the form [[title, text, score, num comments, comment] x N].
"""
def assemble_thread_info(url, header):
    try:
        json_tree = requests.get(url + '.json?limit=200', headers=header)
    except:
        print('caught a bad url')
        return None
    return parse_info(json_tree)

"""
Creates a thread to all assemble_thread_info for each URL passed to it.
"""
def thread_builder(urls, headers):
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as exec:
        futures = [exec.submit(assemble_thread_info, url, headers) for url in urls]
        for future in futures:
            result = future.result()
            if result is not None:
                rows.extend(result)
    return rows

"""
Main method. Creates dataframe and stores it to output file.
"""
def main(urls, headers, output_path):
    rows = thread_builder(urls, headers)
    print(f'parsed {len(rows)} comments in ', end='')  # Debug
    df = pd.DataFrame(rows)
    df.to_csv(output_path)

"""
Prints time taken and comments parsed to stdout.
"""
if __name__ == '__main__':
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
    HEADERS = {'User-agent': 'Reccomeddit-Bot 0.101'}
    start = time.time()  # Debug
    main(URLS, HEADERS, OUTPUT_FILE)
    end = time.time()  # Debug
    print(f'{end-start} seconds')  # Debug
