# YouTube Video: https://www.youtube.com/watch?v=rhBZqEWsZU4
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import re

from textblob import TextBlob



# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user







    def simplyfying_twt_api(self):
        return self.twitter_client



    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):##here friend means followers
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):##  .hometimeline fun passed to client and user set in initialization below
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        api_key = "jVD47CDID0dS0cRN3p1pWLu1O"

        api_token_secret = "Vyv0MQUQRcSQUXCWxfyzEjLDL12lku9zBHgk5B5tPempW8HD23"

        access_token = "1271371802715906049-zyYGcTEb7ifmAZ6yfxXYzyLusBnylh"
        access_secret_token = "8HhgPzPf0i8pYIhzfHx0NEG5tn0IwzbkGnxlF1d4GniPl"
        #listener = TwitterListener(ftchAppFile)#
        auth = OAuthHandler(api_key, api_token_secret)
        auth.set_access_token(access_token, access_secret_token)
        return auth

        return auth


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
       # stream.filter(track=hash_tags)#


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

   # def __init__(self, ftc):
        #self.ftchAppFile = ftchAppFile#

    def on_data(self, data):
        try:
            print(data)
            with open(self.ftchAppFile, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)




class tweetAnalyzer():

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1
    def tweets_to_data_frame(self,tweets):
        df=pd.DataFrame(data=[tweet.text for tweet in tweets],columns=["tweets"])


        df['id']=np.array([tweet.id for tweet in tweets])
        df['len']=np.array([len(tweet.text) for tweet in tweets])
        df['date']=np.array([tweet.created_at for tweet in tweets])
        df['source']=np.array([tweet.source for tweet in tweets])
        df['likes']=np.array([tweet.favorite_count for tweet in tweets])
        df['retweets']=np.array([tweet.retweet_count for tweet in tweets])


        return df






if __name__ == '__main__':
    # Authenticate using config.py and connect to Twitter Streaming API.
    twitter_Client=TwitterClient()
    api= twitter_Client.simplyfying_twt_api()
    tweet_yaha_anay=tweetAnalyzer()
    tweets=api.user_timeline(screen_name="pycon",count=200)

    df=tweet_yaha_anay.tweets_to_data_frame(tweets)



    print(df.head(20))

    print(np.mean(df['len']))
    print(np.max(df['likes']))

    #time_likes =pd.Series(data=df['likes'].values , index=df['date'])
    #time_likes.plot(figsize=(16,4),color='r')
    #plt.show()
    #time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    #time_retweets.plot(figsize=(16, 4), color='r')
    #plt.show()

   ## Layered Time Series:
    time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    time_likes.plot(figsize=(16, 4), label="likes", legend=True)

    #time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    #time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
    #plt.show()

    df['sentiment'] = np.array([tweet_yaha_anay.analyze_sentiment(tweet) for tweet in df['tweets']])

   # print(tweets[0].id)
    print(df.head(10))