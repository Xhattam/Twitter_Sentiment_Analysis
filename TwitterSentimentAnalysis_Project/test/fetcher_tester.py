from fetcher import TwitterClient
import unittest
import json


class TestTwitterClient(unittest.TestCase):

    def test_number_tweets(self):
        """ Are we getting the number of tweets we asked for """
        tc = TwitterClient()
        tweets = tc.get_raw_tweets(['babylonhealth'], 10)
        self.assertEqual(len(tweets), 10)

    def test_concent(self):
        """ Do the tweets we get contain the query, or are published by the term in the query """
        tc = TwitterClient()
        tweets = tc.get_raw_tweets(['babylonhealth'], 10)
        a = sum([1 for t in tweets if 'babylonhealth' in json.dumps(t)])
        self.assertEqual(a, 10)


