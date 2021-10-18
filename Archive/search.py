import os

# the hide api key bs
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv(".env")
my_api_key = os.getenv("SEARCH_PY_API_KEY")
cx_key = os.getenv("CX_KEY")
################################################################

resource = build("customsearch", "v1", developerKey=my_api_key).cse()


# search google with string and make sure has reddit in it
# return list of urls with reddit links
# they will do their magic with the reddit links


def return_links(searchstring):
    result = resource.list(q=searchstring + " reddit", cx=cx_key).execute()
    linkarray = []
    for item in result["items"]:
        url = item[
            "link"
        ]  # link is url (e.g., https://www.reddit.com/r/fountainpens/comments/13isgr/guide_to_getting_your_first_fountain_pen)
        domain = item["displayLink"]  # displayLink is domain (e.g., www.reddit.com)
        if domain.endswith("reddit.com") and "comments" in url:
            linkarray.append(url)
    return linkarray
