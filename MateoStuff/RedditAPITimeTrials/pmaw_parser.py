from functional import seq
from pmaw import PushshiftAPI

from utils import url_to_submission_id, urls, url_to_subreddit, comment_to_dict

api = PushshiftAPI()


def parse_with_pmaw():
    comments = (seq(urls)
                .map(lambda url: (url_to_submission_id(url), url_to_subreddit(url)))
                .smap(lambda submission_id, subreddit:
                      api.search_comments(subreddit=subreddit, link_id=submission_id))
                .map(comment_to_dict)
                .to_list())
    return comments


def parse_with_two_step_pmaw():
    post_ids = seq(urls).map(url_to_submission_id)
    comment_ids = api.search_submission_comment_ids(ids=post_ids)
    comments = api.search_comments(ids=comment_ids)
    comment_list = [comment_to_dict(comment) for comment in comments]
    return comment_list
