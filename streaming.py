import tweepy
import process_tweet
import sqlite3 as lite
import sys
import datetime

access_token = "388580420-Re8e1d6eMm5JS1zRKIlzrfmbkgGGwj8qHTZGeE9J"
access_token_secret = "UpaHOEq2Rmf3H1AVWi9evJZazVvyninIt9AoiSixGLLDp"
consumer_key = "7njFqj4sWSWEbpiaVvcZ8AghN"
consumer_secret = "4JIWmXdwDFvxoldR95ggXMliKSSPTA0nPReTWp7oJXdMf4K9Se"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def start_stream():
    while True:
        try:
            myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
            #This is molly's account
            myStream.filter(follow=['1198917355'])
            #This is my test account
            #myStream.filter(follow=['759886618325053440'])
        except:
            print "Stream Error encountered... Restarting stream", datetime.datetime.now()
            continue 


#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.user.id_str == '1198917355':
            currID =0
            #TODO: add follower_count at time of tweet to Database
            #TODO: add tweet media to database when tweets are downloaded
            print status.text
            process_tweet.processTweet('full_db.db',status,'Tweets')
        
print "Streaming Tweets to Database....", datetime.datetime.now() 
myStreamListener = MyStreamListener()
# There is an issue sometimes with trying to use the filter, when using the filter the process simply ends, which is undesired
#This issue is most likely a result of the stream already running in the background or twitter streaming rate limits

start_stream()
print "Fuck, You weren't supposed to see this, something went wrong", datetime.datetime.now()
