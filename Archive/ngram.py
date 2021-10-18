import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from nltk.corpus import stopwords 

#removing stopwords(if but we he she)
english_stop_words = stopwords.words('english')
def remove_stop_words(corpus):
    removed_stop_words = []
    for review in corpus:
        removed_stop_words.append(
            ' '.join([word for word in review.split()
                        if word not in english_stop_words]))
    return removed_stop_words

#print(remove_stop_words('bromwell high is a cartoon comedy'))

def stemming():
    return 0
                        
def split(inputstring):
    wordlist = inputstring.split()
    return wordlist
def getNGrams(wordlist, n): #wordlist is split words, n is the n in n-gram
    ngrams = []
    letters = list(wordlist)
    for i in range(len(letters) - (n-1)):
        ngrams.append(letters[i:i+n])
    return ngrams

#teststring = 'hello it is a very nice day'
#print(getNGrams(list(teststring.split()),3))

cv = CountVectorizer(ngram_range = (2,2))
corpus = ['this is a sentence is', 'this is another sentence',
    'this is the third sentence']
# X = cv.fit(corpus)
# X = cv.transform(corpus)
# print(X.shape)
# print(X)
# print(X.toarray())
# df = pd.DataFrame(X.toarray(),columns = cv.get_feature_names())
# print(df)
with open('sample.txt', 'r') as file:
    data = file.read()
data = [data]
def run(datasample): #datasample = array of strings
    data = datasample
    cv2 = CountVectorizer(ngram_range = (2,2))
    X = cv2.fit_transform(data)
    #print(X.toarray())
    df = pd.DataFrame(X.toarray(),columns = cv2.get_feature_names())
    df.head(10)
    return df
run(corpus)