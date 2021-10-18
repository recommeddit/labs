import nltk
import truecase
from nltk.corpus import movie_reviews
#nltk.download('punkt')

sentence = 'michael jackson AnD His Dog like To eat At mcDonalds'
text_to_tag = nltk.word_tokenize(truecase.get_true_case(sentence))

#print(nltk.pos_tag(text_to_tag))

print(dir(movie_reviews))
