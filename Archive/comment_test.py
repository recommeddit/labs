import comment_sentiment as c_s
import time

def runCommentSentiment():
	start_time = time.time()
	exampleComment = "I'd say Infinity War is a better structured movie. It's pacing is perfect, the tone is consistent, and it flows through good. However, I find Endgame a bit better because of everything that happens in it. It's more messy pacing allows for more fanservice and more 'Thor arrives in Wakanda' moments. Most of the characters had satisfying endings and the movie all around was enjoyable. I'll probably never experience another cinematic event like this due to audience reactions and shock value."

	keywords = ['Infinity War', 'Endgame']

	print("Keywords: Infinity War, Endgame")
	print("Comment: ", exampleComment)
	print("Reddit Upvotes: 602")
	print(c_s.get_scores(keywords, exampleComment, 602))
	print(time.time()-start_time)

runCommentSentiment()
