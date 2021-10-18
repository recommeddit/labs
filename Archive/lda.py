#lda technique to extract keywords
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import pandas as pd
import nltk
#nltk.download('wordnet')
stemmer = SnowballStemmer('english')

def lemmatize(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text,pos = 'v')) # the v stands for verbs

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize(token)),
    
    return result

#print(lemmatize('missing'))
# example = 'I have to write this paper for this class'
# words = []
# for word in example.split(' '):
#     words.append(word)
# print(words)
# print(preprocess(example))

with open('sample4.txt', 'r') as file:
    data = file.read()
data = preprocess(data)
data = [data]
#print(data)

#print(data[:2])
# data = ['how','how','is','really','world']
dictionary = gensim.corpora.Dictionary(data)

#print(dictionary["miss"])
# count = 0
# for k,v in dictionary.iteritems():
#     print(k,v)
#     count += 1
#     if count > 20:
#         break

#work on COUNT of most common words 


bow_corpus = [dictionary.doc2bow(text) for text in data]
document_num = 0
bow_doc_x = bow_corpus[document_num]

# print(bow_corpus)
# for i in range(len(bow_corpus[0])):
#     print("Word {} (\"{}\") appears {} time.".format(
#         bow_corpus[0][i][0], dictionary[bow_corpus[0][i][0]], bow_corpus[0][i][1]
#     ))

hashed_corpus = [dictionary.doc2bow(text) for text in data]
lda_model = gensim.models.LdaMulticore(hashed_corpus, num_topics = 1,
    id2word = dictionary, passes = 1, workers = 1)

for idx, topic in lda_model.print_topics(-1):
    print("Topic: {} \nWords: {}".format(idx, topic))
    print("\n")