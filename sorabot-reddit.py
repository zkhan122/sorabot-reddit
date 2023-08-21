import praw
import random
import time
import os
import numpy as np
import statistics as stats
from itertools import islice
from nltk.sentiment import SentimentIntensityAnalyzer

# https://www.reddit.com/prefs/apps

class Bot():
    def __init__(self, client_id, client_secret, user_agent, username, samples,
    subreddit_name):
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.username = username
        self.samples = samples
        self.subreddit_name = subreddit_name
    

    def sentiment(self, string):
        stream = SentimentIntensityAnalyzer()
        analysis = stream.polarity_scores(string)
        
        pos_score = analysis["pos"]
        neg_score = analysis["neg"]

        return tuple((pos_score, neg_score)) 

    
    def result(self, buffer, pos_score, neg_score):
        outcome_feed = ""
        if pos_score > neg_score:
            buffer.append("POSITIVE")
        elif neg_score > pos_score:
            buffer.append("NEGATIVE")
        else:
            buffer.append("BALANCED")
        
        return buffer
    
    def run(self):
        reddit = praw.Reddit(
        client_id= self.client_id,
        client_secret= self.client_secret, 
        user_agent= self.user_agent, 
        username= self.username)

        subreddit_channel = reddit.subreddit(self.subreddit_name)
        print(subreddit_channel)
        
        sentiment_buffer = []
        i = 1
        for post in subreddit_channel.hot(limit=self.samples):
            print("---------------------------------" + "\n")
            print("POST " + str(i) + " " + str(post.title))
            print("Link: " + str(post.url) + "\n") # grabbing the title

            for comment in post.comments:
                if hasattr(comment, "body"):
                    comment_lower = comment.body.lower()
                    print("-------------------------------")
                    print("Comment: " + str(comment.body)) # grabbing comments 

                    comment_feed = []            
                    comment_feed.append(comment_lower)
                    
            # adding the sentiment scores of comments with body to the buffer
            buffer = [(self.sentiment(comment.body.lower())) for comment in post.comments if
                                hasattr(comment,"body")]
            
            pos_prediction_buffer = []
            neg_prediction_buffer = []

           # print(buffer)
            
            for scores in buffer:
                pos_prediction_buffer.append(scores[0]) # positive scores array
                neg_prediction_buffer.append(scores[1]) # negative scores array
                
            # finding the mean for each buffer
            score_1 = stats.mean(pos_prediction_buffer)
            score_2 = stats.mean(neg_prediction_buffer)
            # reassigning back into same buffer
            sentiment_buffer = self.result(sentiment_buffer, score_1, score_2)
            
            i += 1
            time.sleep(5) # add delay


        print()
        print("---------------")
        for post_idx, _ in enumerate(sentiment_buffer):
            print("GENERAL CONSENSUS FOR POST " + str(post_idx+1) + ": " + str(_))



if __name__=="__main__":
    # CHANGE PARAMETERS (read README.md)
    bot = Bot(client_id="",
              client_secret="",
              user_agent="",
              username="", samples=0, subreddit_name="") 
    bot.run()

