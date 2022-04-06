import pandas as pd
import scoring
import csv
import time
import numpy as np

start = time.time()

df = pd.read_csv('/mnt/c/Users/adity/Downloads/comments_with_ents.csv')

sentiment_scores = []
upvotes = np.random.randint(100, size=len(df))

for i in range(len(df)):
    comment = df.loc[i, 'comments']
    scores = scoring.calc_points(comment, upvotes[i])
    #print(scores)
    sentiment_scores.append(scores)

print(time.time()-start)

# titles = ['pos','neu','neg']

# with open('/mnt/c/Users/adity/Downloads/sa_test.csv', 'w') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=titles)
#     writer.writeheader()
#     writer.writerows(sentiment_scores)


