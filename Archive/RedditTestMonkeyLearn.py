from MonkeyLearnProductSentiment import *

def get_post(url):
    """
    Get a map of <comments, votes> from post url
    """
    import comments
    reddit = comments.connect()
    comments = comments.get_comments(reddit, url)
    #print(comments)
    return comments

post = get_post("https://www.reddit.com/r/learnpython/comments/ktjtl5/best_ide_for_python/")
#print(type(post))

#print(post.keys)
#separated_strings = seperate_into_strings(post[)
#print(post.keys())

entities = []
for comment in post.keys():
    doc = seperate_into_strings([comment])

    entities.append(doc)
#print(entities)
array = []
for a in entities:
    array.append(keyword_extractor(a))
new_array = []
for i in array:
    if (len(array[i] >= 2)):
        new_array.append(array[i][0])

print(new_array)


