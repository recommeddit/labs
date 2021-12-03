"""
Testing Only
"""
def reg(url):
    return requests.get(url, headers = {'User-agent': 'testing 0.1'})

def test_regular(urls):
    return [requests.get(url, headers = {'User-agent': 'testing 0.1'}) for url in urls]

def test_session(urls):
    main_url = 'https://www.reddit.com'
    s = requests.Session()
    return [s.get(url, headers = {'User-agent': 'testing 0.1'}) for url in urls]

def test_parallel(urls):
    with multiprocessing.Pool(len(urls)) as p:
        return list(p.map(reg, urls))

def test_parallel_session(urls):
    main_url = 'https://www.reddit.com'
    s = requests.Session()
    with multiprocessing.Pool(len(urls)) as p:
        return list(p.map(reg, urls))

def test_threading(urls):
    def fun(url):
        return requests.get(url, headers = {'User-agent': 'testing 0.1'})
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as x:
        data = x.map(fun, urls)
    return list(data)

def time_it(f, param):
    start = time.time()
    print(f.__name__, f(param))
    print(f'total time: {time.time() - start}')

def main():
    functions = [test_regular, test_session, test_parallel, test_parallel_session, test_threading]
    #functions = [test_threading]
    #functions = [test_session, test_parallel, test_parallel_session]
    urls = ["https://www.reddit.com/r/movies/comments/2isv8p/what_are_some_good_mindfuck_movies_like_inception/",
            "https://www.reddit.com/r/MovieSuggestions/comments/n5w7p3/movies_similar_to_inception/",
            "https://www.reddit.com/r/NetflixBestOf/comments/8l7g9t/request_mindmelting_movies_similar_to_inception/",
            "https://www.reddit.com/r/movies/comments/cbxpnj/movies_like_interstellar_inception_and_arrival/",
            "https://www.reddit.com/r/movies/comments/g4jrx8/movie_recommendations_similar_to_ex_machina/",
            "https://www.reddit.com/r/AskReddit/comments/4gib6l/what_are_some_mindfuck_movies_like_shutter_island/",
            "https://www.reddit.com/r/booksuggestions/comments/k7x6xv/recommend_a_book_like_movies_inception/",
            "https://www.reddit.com/r/movies/comments/e3kndv/looking_for_great_movies_with_great_music_like/",
            "https://www.reddit.com/r/movies/comments/evryo/inception_picks_up_where_shutter_island_left_off/",
            "https://www.reddit.com/r/movies/comments/1ukv5u/looking_for_some_movies_similar_to_inception/"]
    for f in functions:
        time_it(f, urls)
        time.sleep(1)

if __name__ == '__main__':
    main()
