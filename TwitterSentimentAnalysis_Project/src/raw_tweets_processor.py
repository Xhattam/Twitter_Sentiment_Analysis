import pandas as pd
from textblob import TextBlob
import logging

""" Reads raw tweets extracted by `fetcher`, and formats results in a clean dataframe for later analysis

@author: Jessica Tanon

DATE: MAR 2019
"""

logging.basicConfig(level="INFO")


class Processor:

    def __init__(self):
        self.mapped_months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05','Jun': '06', 'Jul': '07',
                              'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
        self._logger = logging.Logger(name="Processor")

    @staticmethod
    def get_polarity(score):
        """ Returns a polarity value based on the polarity score (subjective)
        :param score: polarity score returned by TextBlob
        :returns: an associated polarity (Positive, Negative, Neutral) """
        if score <= 0.2:
            return "Negative"
        elif score <= 0.7:
            return "Neutral"
        else:
            return "Positive"

    @staticmethod
    def extract_mentions(mentions):
        """ Extract user mentions from a tweet
        :param mentions: list of user mentions (from Twitter API)
        :returns: comma-separated user name and screen names """
        return ", ".join([e['name'] + " (" + e['screen_name'] + ")" for e in mentions])

    def get_readable_date(self, twitter_date):
        """ Extract the date in a friendlier format (dd/mm/yy)
        :param twitter_date: date returned by Twitter API
        :returns: readable date """

        split = twitter_date.split(" ")
        month, value, year = self.mapped_months[split[1]], split[2], split[-1]
        return "/".join([value, month, year])

    def extract_info(self, raw_tweets):
        """ Main extraction function, returns relevant fields for each tweet returned by the
            Twitter API
        :param raw_tweets: list of extracted tweets, in json format
        :returns: dataframe of extracted information """

        self._logger.info("Extracting data from tweets...")

        fields = ['u_name', 'u_screen_name', 't_date', 't_text', 't_polarity_score',
                  't_polarity', 't_subjectivity_score', 'u_followers', 't_retweets',
                  't_favorited', 't_mentions', 't_id']

        all_extracted = {k: [] for k in fields}
        for tweet in raw_tweets:
            all_extracted['u_name'].append(tweet['user']['name'])
            all_extracted['u_screen_name'].append(tweet['user']['screen_name'])
            all_extracted['t_date'].append(self.get_readable_date(tweet['created_at']))
            all_extracted['t_text'].append(tweet['full_text'])

            tb_analysed = TextBlob(tweet['full_text'])
            all_extracted['t_polarity_score'].append(tb_analysed.polarity)
            all_extracted['t_subjectivity_score'].append(tb_analysed.sentiment.subjectivity)
            all_extracted['t_polarity'].append(self.get_polarity(tb_analysed.polarity))
            all_extracted['u_followers'].append(tweet['user']['followers_count'])
            all_extracted['t_retweets'].append(tweet['retweet_count'])
            all_extracted['t_favorited'].append(tweet['favorite_count'])
            all_extracted['t_mentions'].append(self.extract_mentions(
                tweet['entities']['user_mentions']))
            all_extracted['t_id'].append(tweet['id'])

        df = pd.DataFrame(all_extracted)
        return df
