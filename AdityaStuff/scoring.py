from sentence_splitter import SentenceSplitter, split_text_into_sentences
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def average(lst):
    return sum(lst)/len(lst)

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

#def calc_ranks(sentiments):


if __name__ == "__main__":
    comment = "TL;DR In large part I think school rankings are very course-grained. In the US, at least, the top 10-20 schools generally or in a particular category probably belong there, and the top 100 schools probably belong in that range, too. But the differences between the 2nd and the 5th or the 32nd and the 47th are not likely of any significance, at least not as measured by the rankings."
    sentiments = get_sentiment_scores(comment)
    import pdb;pdb.set_trace()