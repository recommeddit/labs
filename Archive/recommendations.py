import html

from functional import seq

import MonkeyLearnProductSentiment
import comments
import markdown_to_plaintext
import search

MAX_CHARS = 42000


def get_recommendations(query):
    if not query:
        return {"error_message": "No query", "success": False, "recommendations": []}

    # search google for "<query name> reddit"
    reddit_urls = search.return_links(query)

    # resolve reddit URLs to comments and remove HTML/markdown syntax
    reddit = comments.connect()
    all_comments = (
        seq(reddit_urls)
            .flat_map(lambda reddit_url: comments.get_comments(reddit, reddit_url))
            .map(lambda comment: comment["text"])
            .map(html.unescape)
            .map(markdown_to_plaintext.unmark)
    )

    chunked_all_comments = []
    for comment in all_comments:
        if not chunked_all_comments:
            chunked_all_comments.append(comment)
        else:
            newline_and_comment = "\n\n" + comment
            if len(chunked_all_comments[-1] + newline_and_comment) > MAX_CHARS:
                chunked_all_comments.append(comment)
            else:
                chunked_all_comments[-1] += newline_and_comment

    results = MonkeyLearnProductSentiment.keyword_extractor_total(
        chunked_all_comments, []
    )

    return {"error_message": "", "success": True, "recommendations": results}
