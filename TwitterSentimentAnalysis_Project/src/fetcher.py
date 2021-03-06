import tweepy
from tweepy import OAuthHandler
import json
import logging

""" Twitter authentication and tweets fetcher class.

@author: Jessica Tanon

DATE: March 2019
"""

logging.basicConfig(level="INFO")


class TwitterClient(object):
    """ Authenticate, and get tweets from Twitter """

    def __init__(self):

        keys = json.load(open("../resources/twitter_keys.json", "r"))
        consumer_key = keys['consumer_key']
        consumer_secret = keys['consumer_secret']
        acces_token = keys['access_token']
        access_token_secret = keys['access_token_secret']
        self._logger = logging.Logger(name="TwitterClient")

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(acces_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except Exception as e:
            print("Authentication failed: {}".format(e))

    def get_raw_tweets(self, query, count):
        """ Main function to fetch tweets and parse them.
        :param query    : seach query
        :type query     :str
        :param count    : number of tweets to fetch
        :type count     : int
        :returns: list of unique tweets """

        #  empty set to store parsed tweets (unique)
        tweets = []
        self._logger.info("Querying Twitter...")
        try:
            #  call twitter api to fetch tweets
            fetched_tweets = [status for status in tweepy.Cursor(
                self.api.search, q=query, tweet_mode='extended').items(count)]

            for tweet in fetched_tweets:
                tweets.append(tweet._json)

            self._logger.info("Fetched {}/{} tweets".format(len(fetched_tweets), count))

            self._logger.info("Writing fetched tweet to json file...")
            return tweets

        except tweepy.TweepError as e:
            self._logger.error("Error fetching tweets: " + str(e))
