#!/usr/bin/env python
# coding: utf-8

# In[4]:


pip install google-search-results


# In[5]:


pip install monkeylearn


# In[1]:


from monkeylearn import MonkeyLearn
from serpapi import GoogleSearch


# In[37]:


#example query
query = "what are the best computers to use"

#example of list of recommendations
recommendations = ["dell","chromebook","apple"]

#params for serp_image api
params = {
    "q": [],
    "tbm": "isch",
    "ijn": "0",
    "api_key": "0b76a3167c55fc6256f009764b9badb03a03a6afc41da80d11e3a14dd0080520"
}

#function to get keywords from query using monkeylearn api 
#1000 queries per month could use a different one if we need to
def get_keywords(query):
    ml = MonkeyLearn('9edf66714f7d18a9b8da526770bd4b5559b61b90')
    data = [query]
    model_id = 'ex_YCya9nrn'
    result = ml.extractors.extract(model_id, data)
    for x in result.body:
        extracted = (x['extractions'])
        for words in extracted:
            key_words = (words['parsed_value'])
        return str(key_words)

#function to get images/description of images 
#based off a list of recommendations and keywords extracted from query
def get_images(query,recommendations):
    key_words = get_keywords(query)
    recommendations_list = len(recommendations)
    x = 0 
    while x<recommendations_list:
        for g in recommendations:
            params["q"] = g+key_words
            search = GoogleSearch(params)
            results = search.get_dict()
            images_results = results['images_results']
            first_image=images_results[1]
            print(first_image['thumbnail'])
            x=x+1
    

get_images(query,recommendations)
#I still need to configure it with the actual code for the recommeddit itself


# In[ ]:




