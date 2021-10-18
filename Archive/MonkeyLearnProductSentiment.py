from monkeylearn import MonkeyLearn
from functional import seq

# hide api
import os
from dotenv import load_dotenv

load_dotenv(".env")
api_key = os.getenv("URL_SCRAPE_API_KEY")
################################################################

# temporary using api key, change this to .env later on
ml = MonkeyLearn(api_key)


def returnMonkey(data):
    # model id for Product Sentiment
    model_id = "cl_TWmMTdgQ"
    result = ml.classifiers.classify(model_id, data)

    return result.body[0]["classifications"][0]


# print(returnMonkey(['This is the best IDE']))
def returnPositiveorNot(data):
    # will return either positive neutral or negative
    PositiveorNot = returnMonkey(data)["tag_name"]
    return PositiveorNot


# print(returnPositiveorNot(['This is the best IDE']))


def returnConfidence(data):
    # returns confidence in percentage
    confidence = returnMonkey(data)["confidence"]
    # confidence = "{:.1%}".format(0.999)
    return confidence


# print(returnConfidence(['laughing out loud']))

################################################################
# seperate data into strings


def seperate_into_strings(text):
    # uses monkeylearn to extract OPINION units from text
    # text is our input, a big reddit comment that may have multiple sentences
    model_id = "ex_N4aFcea3"
    result = ml.extractors.extract(model_id, text)
    # total is the extractions
    total = result.body[0]["extractions"]
    # data is an array of parsed sentences of the original text
    data = []
    for i in range(len(total)):
        data.append(total[i]["extracted_text"])
    return data


"""
print(seperate_into_strings(['The hotel has a great location but all in all it was a horrible experience! \
    Only stayed here because it was the pre-accomodation choice for one of our tours but it was terrible. \
        Will never stay here again!'])[0])
"""
################################################################
# THIS USES THE KEYWORD EXTRACTOR I DON'T KNOW HOW WELL THIS WILL WORKS
# MAY HAVE A PROBLEM WITH DETECTING TOO MANY KEYWORDS
# MAYBE I CAN INCLUDE VALUES WITH A CERTAIN AMOUNT OF RELEVANCE
def keyword_extractor(data):
    model_id = "ex_YCya9nrn"
    result = ml.extractors.extract(model_id, data)
    array_of_keywords = []
    # total is the extractions
    total = result.body[0]["extractions"]
    # appends the top value because I think it automatically sorts by relevance
    for i in range(len(total)):
        array_of_keywords.append(total[i]["parsed_value"])
    return array_of_keywords


def keyword_extractor_total(data, list_of_comment_bounds):
    model_id = "ex_YCya9nrn"
    results = ml.extractors.extract(model_id, data).body

    analyzed_comments = []
    for result in results:
        extracted_keywords = result.extractions
        chunked_comment = result.text

        upper_bound = len(chunked_comment)
        for comment_bounds in list_of_comment_bounds:
            if comment_bounds[1] > upper_bound:
                break
            analyzed_comments.append(
                {
                    "comment": chunked_comment[comment_bounds[0] : comment_bounds[1]],
                    "lower_bound": comment_bounds[0],
                    "upper_bound": comment_bounds[1],
                    "keywords": set(),
                }
            )

        for keyword in extracted_keywords:
            for position in keyword["positions_in_text"]:
                comment_with_keyword = next(
                    (
                        comment
                        for comment in analyzed_comments
                        if comment.lower_bound <= position <= comment.upper_bound
                    ),
                    None,
                )
                if comment_with_keyword is not None:
                    comment_with_keyword["keywords"].add(keyword)

    # convert keywords back to a set (they were sets in the first place to dedupe)
    for comment in analyzed_comments:
        comment.keywords = list(comment.keywords)

    return analyzed_comments


# print(keyword_extractor(['This error is caused because we try to convert “7.4: to an integer.']))
# test = [
#     "Elon Musk has shared a photo of the spacesuit designed by SpaceX. This is the second image shared of the new design and the first to feature the spacesuit",
#     "I use Kaleidoscope\n\nhttp://www.kaleidoscopeapp.com/\n\nThis is a file comparison tool which is excellent at helping you merge and can serve many other purposes. Not an all-in-one git client like some of the other replies",
# ]
# print(keyword_extractor_total(test))