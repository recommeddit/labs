import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

analyzer = SentimentIntensityAnalyzer()
#nltk.download('vader_lexicon')

def average(lst):
	return sum(lst)/len(lst)

def adjust_upvotes(upvotes):
	if upvotes > 0 and upvotes <= 100:
		score = upvotes
	elif upvotes > 100 and upvotes <= 1000:
		score = 100 + (upvotes - 100)*0.25
	elif upvotes > 1000 and upvotes <= 10000:
		score = 100 + (900*0.25) + (upvotes - 1000)*0.1
	elif upvotes > 10000:
		score = 100 + (900*0.25) + (9000*0.1) + (upvotes - 10000)*0.01

	return score

def get_sentiment_scores(comment):
	avg_sentiments = {}
	pos_scores = []
	neu_scores = []
	neg_scores = []

	sentences = re.split('(?<=[\.\?\!])\s*', comment)

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
	"""
	pass in comment.sentences
	"""
	sa_scores = get_sentiment_scores(comment)
	score = adjust_upvotes(upvotes)
	points = (2*sa_scores['pos'] + 1*sa_scores['neu'] - 3*sa_scores['neg'])*score
	return points

if __name__ == "__main__":
	print(adjust_upvotes(30547))
