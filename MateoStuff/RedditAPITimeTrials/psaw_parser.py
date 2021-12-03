from functional import seq
from psaw import PushshiftAPI

from utils import urls, url_to_subreddit, comment_to_dict, url_to_submission_id

api = PushshiftAPI()


def parse_with_psaw():
    comments = (seq(urls)
                .map(lambda url: (url_to_submission_id(url), url_to_subreddit(url)))
                .smap(lambda submission_id, subreddit:
                      api.search_comments(subreddit=subreddit, link_id=submission_id))
                .map(comment_to_dict)
                .to_list())
    return comments
