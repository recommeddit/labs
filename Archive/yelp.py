import requests

import os
from dotenv import load_dotenv
load_dotenv('.env')

from YelpAPI import yelpkey

#define a business id to
business_id = '4AErMBEoNzbk7Q8g45kKaQ'

#
API = yelpkey
ENDPOINT = "https://api.yelp.com/v3/businesses/search"

