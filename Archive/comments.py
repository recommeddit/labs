import praw
import logging
import os
from dotenv import load_dotenv
from functional import seq

load_dotenv(".env")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
USER_AGENT = os.getenv("USER_AGENT")


# from praw.models import MoreComments


def enable_praw_log():
    """
    Enables PRAW HTTP logging
    See https://praw.readthedocs.io/en/latest/getting_started/logging.html
    :return:
    """
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    for logger_name in ("praw", "prawcore"):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)


def connect() -> praw.Reddit:
    """
    Code flow: connect to reddit api without an account
    :return: bool
    """
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        user_agent=USER_AGENT,
    )
    # print(reddit.auth.url(["identity"], "...", "permanent"))
    print("User:", reddit.user.me())
    # print("Access to:", reddit.auth.scopes())

    reddit.read_only = True
    return reddit


def comment_to_dict(comment):
    return {
        "text": comment.body,
        "score": comment.score,
        "url": "https://www.reddit.com" + comment.permalink,
    }


def get_comments(reddit, url: str) -> list:
    """
    Get all comments from a particular URL.
    Currently added by BFS order.
    :param url:
    """
    submission = reddit.submission(url=url)
    submission.comments.replace_more(
        limit=None
    )  # removes limit=x amount of MoreComments

    comments = seq(submission.comments.list()).map(comment_to_dict)

    return comments


def post_to_dict(post):
    return {
        "text": post.selftext,
        "score": post.score,
        "url": post.url,
    }


def get_post(reddit, url: str):
    """
    Get post content and votes
    :param reddit:
    :param url:
    :return: list: post, upvotes, url
    """
    submission = reddit.submission(url=url)
    return post_to_dict(submission)


# enable_praw_log()
# reddit = connect()
# test_url = "https://www.reddit.com/r/cpp/comments/1rml6l/good_books_on_distributedparallel_systems/"
# post = get_post(reddit, test_url)
# print(post)
