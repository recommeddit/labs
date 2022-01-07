import json
import time

import requests
from functional import seq

from utils import urls, url_to_submission_id, url_to_subreddit, comment_to_dict

ID_LENGTH = 6


def get_comments_from_url(url: str) -> list:
    submission_id = url_to_submission_id(url)
    subreddit = url_to_subreddit(url)
    pushshift_url = f"https://api.pushshift.io/reddit/comment/search/?subreddit={subreddit}&link_id={submission_id}&limit=1000"
    request_start = time.time()
    submission = requests.get(pushshift_url)
    submission_results = []
    try:
        submission_results = json.loads(submission.content)['data']
    except json.decoder.JSONDecodeError:
        print(f"ERROR: JSONDecodeError for {url}")
        print(f"response: {submission.content}")
    num_results = len(submission_results)
    while num_results == 100:
        pushshift_url = f"https://api.pushshift.io/reddit/comment/search/?subreddit={subreddit}&link_id={submission_id}&limit=1000&until={submission_results[-1]['created_utc']}"
        request_end = time.time()
        time.sleep(max(0., 0.7 - (request_end - request_start)))
        request_start = time.time()
        submission = requests.get(pushshift_url)
        additional_results = []
        try:
            additional_results = json.loads(submission.content)['data']
        except json.decoder.JSONDecodeError:
            print(f"ERROR: JSONDecodeError for {url}")
            print(f"response: {submission.content}")
        num_results = len(additional_results)
        submission_results += additional_results
    request_end = time.time()
    time.sleep(max(0., 0.7 - (request_end - request_start)))

    comments = seq(submission_results).map(comment_to_dict)
    return comments


def parse_with_raw_pushshift_api():
    comments = seq(urls).map(get_comments_from_url)
    return comments
