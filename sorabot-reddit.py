import praw
import random
import time

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
    
    def run(self):
        reddit = praw.Reddit(
        client_id= self.client_id,
        client_secret= self.client_secret, 
        user_agent= self.user_agent, 
        username= self.username)

        subreddit_channel = reddit.subreddit(self.subreddit_name)
        print(subreddit_channel)
        
        i = 1
        for post in subreddit_channel.hot(limit=self.samples):
            print("---------------------------------" + "\n")
            print("POST " + str(i) + " " + str(post.title))
            print("Link: " + str(post.url) + "\n") # grabbing the title

            for comment in post.comments:
                if hasattr(comment, "body"):
                    comment_lower = comment.body.lower()
                    print("-------------------------------")
                    print("Comment: " + str(comment.body)) 
            i += 1
            time.sleep(10)

if __name__=="__main__":
    bot = Bot(client_id="", client_secret="",
               user_agent="",
               username="", samples=__, subreddit_name="") # replace with own args

    bot.run()
