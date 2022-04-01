import pandas as pd
import scoring
import csv

df = pd.read_csv('/mnt/c/Users/adity/Downloads/comments_with_ents.csv')

sentiment_scores = []

for i in range(len(df)):
    comment = df.loc[i, 'comments']
    scores = scoring.get_sentiment_scores(comment)
    sentiment_scores.append(scores)

titles = ['pos','neu','neg']

with open('/mnt/c/Users/adity/Downloads/sa_test.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=titles)
    writer.writeheader()
    writer.writerows(sentiment_scores)


