from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
from nltk.tokenize import TweetTokenizer, sent_tokenize
import nltk
import random as rd
import time

def get_comment_sentiment(comment, keywords, upvotes):
	tokenizer_words = TweetTokenizer()
	tokens_sentences = [tokenizer_words.tokenize(t) for t in nltk.sent_tokenize(comment)]
	sentence = ""
	sentenceStruct, rawScores= [], []
	sentenceScore = 0
	keywordDetected = False
	start_time = time.time()
	for ind in range(0, len(tokens_sentences)):
		keywordDetected = False
		sentenceStruct = tokens_sentences[ind]
		sentence = " ".join(sentenceStruct)
		sentenceScore = sentiment_scores(sentence, upvotes)
		for word in sentenceStruct:
			for keyword in keywords:
				if keywordDetected == False:
					if keyword.casefold() == word.casefold():
						rawScores += (keyword, sentenceScore)
						keywordDetected = True
		if keywordDetected == False:
			rawScores += ('sentence', sentenceScore)
	#print(time.time()-start_time)

	midScores = []
	currKey = 'placeholder'
	currScore = 0.0
	counter = 0
	#start_time = time.time()
	for ind in range(0, len(rawScores)):
		if (type(rawScores[ind]) is str) & (rawScores[ind] != 'sentence'):
			if currKey == 'placeholder':
				currKey = rawScores[ind]
				currScore += rawScores[ind+1]
				counter += 1
			elif rawScores[ind] != currKey:
				midScores += (currKey, currScore/counter)
				currKey = rawScores[ind]
				currScore = 0.0
				currScore += rawScores[ind+1]
				counter = 1
			else:
				currScore += rawScores[ind+1]
				counter += 1
		elif rawScores[ind] == 'sentence':
			currScore += rawScores[ind+1]
			counter += 1
	midScores += (currKey, currScore/counter)
	#print(time.time()-start_time)

	finalScores, coveredWords = [], []
	currKey = midScores[0]
	currScore = midScores[1]
	counter = 1
	scoreAdded = False
	#start_time = time.time()
	for ind in range(0, len(midScores)):
		if (type(midScores[ind]) is str) & (midScores[ind] not in coveredWords):
			coveredWords += [midScores[ind]]
			currKey = midScores[ind]
			currScore = midScores[ind+1]
			counter = 1
			scoreAdded = False
			for ell in range(ind+2, len(midScores)):
				if (type(midScores[ell]) is str):
					if (midScores[ell] == currKey) & (ell != (len(midScores)-2)):
						currScore += midScores[ell+1]
						counter += 1
					elif (midScores[ell] == currKey) & (ell == (len(midScores)-2)):
						currScore += midScores[ell+1]
						counter += 1
						finalScores += (currKey, currScore/counter)
						scoreAdded = True
						break
			if scoreAdded is False:
				finalScores += (currKey, currScore/counter)
	print(time.time()-start_time)
	return finalScores

def sentiment_scores(sentence, upvotes): 
	sid_obj = SentimentIntensityAnalyzer() 
	sentiment_dict = sid_obj.polarity_scores(sentence)
	pos = sentiment_dict['pos']
	neu = sentiment_dict['neu']
	neg = sentiment_dict['neg']
	score = (2*neu*upvotes) + (pos*upvotes) - (neg*upvotes)
	return score

def simplify_title(titles):
	keywords = []
	titleReferences = []
	simplified = False
	commonWords = 'The the This this Is is A a Of of Into into For for But but And and So so There there Through through As as Like like He he She she They they Them them It it'
	start_time = time.time()
	for ind in range(0, len(titles)):
		simplified = False
		title = titles[ind].split()
		while(simplified == False):
			keyword = title[rd.randint(0,(len(title)-1))]
			if keyword not in commonWords:
				simplified = True
				keywords += [keyword]
		titleReferences += (titles[ind], keyword)
	print(time.time()-start_time)
	return keywords,titleReferences

def get_scores(titles, comment, upvotes):
	keys,titleRefs = simplify_title(titles)
	scores = get_comment_sentiment(comment, keys, upvotes)
	rankings = []
	start_time = time.time()
	for ind in range(0, len(scores)):
		if(type(scores[ind]) is str):
			if(scores[ind] == titleRefs[ind+1]):
				rankings += (titleRefs[ind], scores[ind+1])
	print(time.time()-start_time)
	return rankings
		


