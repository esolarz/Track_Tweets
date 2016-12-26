#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "388580420-Re8e1d6eMm5JS1zRKIlzrfmbkgGGwj8qHTZGeE9J"
access_token_secret = "	UpaHOEq2Rmf3H1AVWi9evJZazVvyninIt9AoiSixGLLDp"
consumer_key = "O3hHGETYbEsq0rs2qFzcb44MB"
consumer_secret = "4ETzJlmYdeGYG7NScUvs1JFTcesNaq515tGxCQqa2JlLwCcbEg"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])
