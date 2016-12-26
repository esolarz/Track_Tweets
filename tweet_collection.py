import tweepy
import process_tweet 
import datetime

access_token = "388580420-Re8e1d6eMm5JS1zRKIlzrfmbkgGGwj8qHTZGeE9J"
access_token_secret = "UpaHOEq2Rmf3H1AVWi9evJZazVvyninIt9AoiSixGLLDp"
consumer_key = "7njFqj4sWSWEbpiaVvcZ8AghN"
consumer_secret = "4JIWmXdwDFvxoldR95ggXMliKSSPTA0nPReTWp7oJXdMf4K9Se"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def collect_tweets(table):
    all_tweets = []

    #molly's account
    new_tweets = api.user_timeline(screen_name ='mschwalm',count=200,include_rts = 1)
    #my test account
    #new_tweets = api.user_timeline(screen_name ='Testing32232780',count=200)

    all_tweets.extend(new_tweets)

    oldest = all_tweets[-1].id -1

    while len(new_tweets) >0:
        new_tweets =  api.user_timeline(screen_name = 'mschwalm', count = 200, max_id=oldest,include_rts = 1)
        #new_tweets =  api.user_timeline(screen_name = 'Testing32232780', count = 200, max_id=oldest)

        all_tweets.extend(new_tweets)

        oldest = all_tweets[-1].id -1

        print "...%s tweets downloaded so far" % (len(all_tweets));

    #process tweets in array now
    db = "full_db.db"

    for tweet in all_tweets:
       process_tweet.processTweet(db,tweet,table)
       

    print "Finished collecting tweets", datetime.datetime.now()
    return 

def testCase():
    collect_tweets('Test_Table')
    return

#testCase()
