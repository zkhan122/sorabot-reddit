import praw
import random
import time

# https://www.reddit.com/prefs/apps

class Bot():
    def __init__(self, client_id, client_secret, user_agent, username):
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.username = username
    
    def run(self):
        reddit = praw.Reddit(
        client_id= self.client_id,
        client_secret= self.client_secret, 
        user_agent= self.user_agent, 
        username= self.username)

        subreddit = reddit.subreddit("worldnews")
        print(subreddit)

        for post in subreddit.hot(limit=20):
            print("---------------------------------")
            print(str(post.title))
            print("Link: " + str(post.url) + "\n") # grabbing the title

            for comment in post.comments:
                if hasattr(comment, "body"):
                    comment_lower = comment.body.lower()
                    print("-------------------------------")
                    print("Comment: " + str(comment.body))        


if __name__=="__main__":
    bot = Bot("4u59Mj03AIwY0R55ABs_FQ", "pGB-myBerIjoGk6m57cof6vQH9BOrw",
               "<console:SORA-BOT:1.0>", "Illustrious_Park7068")

    bot.run()
