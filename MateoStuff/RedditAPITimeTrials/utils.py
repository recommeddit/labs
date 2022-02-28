from urllib.parse import urlparse

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


def url_to_submission_id(url):
    """ Returns the unique submission id from the match thread url """
    parsed_url = urlparse(url)
    return parsed_url.path.split('/')[4]


def url_to_subreddit(url):
    """ Returns the subreddit name from the url """
    parsed_url = urlparse(url)
    return parsed_url.path.split('/')[2]


def time(fn):
    """ Decorator to time a function """
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        results = fn(*args, **kwargs)
        end = time.time()
        print(f"{fn.__name__} returned {len(results)} in {end - start} seconds")
        return results

    return wrapper


def comment_to_dict(comment):
    return {
        "text": comment.get("body", ""),
        "score": comment.get("score", 0),
        "url": "https://www.reddit.com" + comment.get("permalink", ""),
    }


def comment_obj_to_dict(comment):
    return {
        "text": comment.body,
        "score": comment.score,
        "url": "https://www.reddit.com" + comment.permalink,
    }
