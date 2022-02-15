from functional import seq
from psaw import PushshiftAPI

from utils import urls, url_to_subreddit, url_to_submission_id, comment_obj_to_dict

api = PushshiftAPI()


def parse_with_psaw():
    comments = (seq(urls)
                .map(lambda url: (url_to_submission_id(url), url_to_subreddit(url)))
                .smap(lambda submission_id, subreddit:
                      list(api.search_comments(subreddit=subreddit, link_id=submission_id)))
                .flatten()
                .map(comment_obj_to_dict)
                .to_list())
    return comments
