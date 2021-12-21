from urllib.parse import urlparse

urls = []


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
