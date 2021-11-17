# imports
from monkeylearn import MonkeyLearn
import requests

# API Stuff
import os
from dotenv import load_dotenv

load_dotenv(".env")
my_api_key = os.getenv("URL_SCRAPE_API_KEY")
url_model_id = "ex_owGiMc4z"
html_model_id = "ex_GdG2eQyy" # html to text model
##############################################################

# return url from comment#
def get_url(userComment):
    ml = MonkeyLearn(my_api_key)
    comment = [userComment]
    url_result = ml.extractors.extract(url_model_id, comment)
    website = url_result.body[0]["extractions"][0]["extracted_text"]
    return website


# add https:// to url if not already present#
def check_url(sitelink):
    substring = "https://"
    valid_site = sitelink.find(substring)
    if valid_site == -1:
        sitelink = substring + sitelink
    return sitelink


# extract and return html from url w/o boilerplate code#
def html_to_text(link):
    ml = MonkeyLearn(my_api_key)
    page = requests.get(check_url(link))
    html_data = page.content
    html_data = [html_data.decode()]
    html_result = ml.extractors.extract(html_model_id, html_data)
    index = 0
    siteText = []
    while True:
        try:
            siteText.append(html_result.body[0]["extractions"][index]["parsed_value"])
            index += 1
        except IndexError:
            break
    return siteText
