import pandas as pd
import scoring
import csv
import time

start = time.time()

df = pd.read_csv('/mnt/c/Users/adity/Downloads/comments_with_ents.csv')

sentiment_scores = []

for i in range(0,500):
    comment = df.loc[i, 'comments']
    scores = scoring.get_sentiment_scores(comment)
    print(scores)
    sentiment_scores.append(scores)

print(time.time()-start)

# titles = ['pos','neu','neg']

# with open('/mnt/c/Users/adity/Downloads/sa_test.csv', 'w') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=titles)
#     writer.writeheader()
#     writer.writerows(sentiment_scores)


