import praw
import random
import time
import os
import numpy as np
from transformers import pipeline
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
    
    def sentiment(self, buffer):
        stream = SentimentIntensityAnalyzer()
        analysis = ""
        for e in range(len(buffer)):
            analysis = stream.polarity_scores(str(e))
        return "Positive:", analysis["pos"], "Negative:", analysis["neg"]


    def villain(self, string):
        stream = SentimentIntensityAnalyzer()
        analysis = stream.polarity_scores(string)
        
        pos_score = analysis["pos"]
        neg_score = analysis["neg"]

        return tuple((pos_score, neg_score)) 

    def run(self):
        reddit = praw.Reddit(
        client_id= self.client_id,
        client_secret= self.client_secret, 
        user_agent= self.user_agent, 
        username= self.username)

        subreddit_channel = reddit.subreddit(self.subreddit_name)
        print(subreddit_channel)
        

        x = None
        i = 1
        for post in subreddit_channel.hot(limit=self.samples):
            # print("---------------------------------" + "\n")
            # print("POST " + str(i) + " " + str(post.title))
            # print("Link: " + str(post.url) + "\n") # grabbing the title

            for comment in post.comments:
                if hasattr(comment, "body"):
                    comment_lower = comment.body.lower()
                    #print("-------------------------------")
                    #print("Comment: " + str(comment.body)) 

                    comment_feed = []            
                    comment_feed.append(comment_lower)
                    

            buffer = [(self.villain(comment.body.lower())) for comment in post.comments if
                                hasattr(comment,"body")]
            
            pos_prediction_buffer = []
            neg_prediction_buffer = []

            print(buffer ,"\n")
            for i in range(len(buffer)):
                for j in buffer[i-1]:
                    pos_prediction_buffer.append(j)
                    neg_prediction_buffer.append(j+1)

            print()
            print("Statistics -> Positive: " +
            str(stats.mean(pos_prediction_buffer))
            + " Negative: " + str(stats.mean(neg_prediction_buffer)))

            # print(self.sentiment(buffer))
        
            i += 1
            time.sleep(5)


        return 0

        
            
if __name__=="__main__":
    bot = Bot(client_id="",
              client_secret="",
              user_agent="",
              username="", samples=0, subreddit_name="")

    print(bot.run())

