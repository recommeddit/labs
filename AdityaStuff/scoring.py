import nltk
import numpy as np
from sentence_splitter import SentenceSplitter, split_text_into_sentences
from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
nltk.download('vader_lexicon')

def average(lst):
	return sum(lst)/len(lst)

def sigmoid(x):
	z = np.exp(-x)
	sig = 1/(1+z)
	return sig

def get_sentiment_scores(comment):
	avg_sentiments = {}
	pos_scores = []
	neu_scores = []
	neg_scores = []

	sentences = split_text_into_sentences(comment, language='en')
	for sentence in sentences:
		sentiment_dict = analyzer.polarity_scores(sentence)
		pos = sentiment_dict['pos']
		neu = sentiment_dict['neu']
		neg = sentiment_dict['neg']

		pos_scores.append(pos)
		neu_scores.append(neu)
		neg_scores.append(neg)
	
	avg_sentiments["pos"] = average(pos_scores)
	avg_sentiments["neu"] = average(neu_scores)
	avg_sentiments["neg"] = average(neg_scores)

	return avg_sentiments

def calc_points(comment, upvotes):
	sa_scores = get_sentiment_scores(comment)
	arg = (2*sa_scores['pos'] + 1*sa_scores['neu'] - 3*sa_scores['neg'])*upvotes
	points = sigmoid(arg)
	return points
