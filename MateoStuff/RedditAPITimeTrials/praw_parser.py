import praw as praw
from functional import seq

from utils import url_to_submission_id, urls, comment_obj_to_dict


def get_all(r, submission_id):
    submission = r.submission(id=submission_id)
    comments_list = []
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        comments_list.append(comment)
    return comments_list


username = 'auto-reddit-rec'
userAgent = "RecommedditScraper/0.1 by " + username
clientId = 'MSo42pflF3S9Ug'
clientSecret = "c6Vmpn6qCFcvEzjw3C-OU2MsOkInWg"
r = praw.Reddit(user_agent=userAgent, client_id=clientId, client_secret=clientSecret)


def parse_with_praw():
    comments = (seq(urls)
                .map(url_to_submission_id)
                .map(lambda submission_id: get_all(r, submission_id))
                .map(comment_obj_to_dict)
                .to_list())
    return comments
