import unittest
import pandas as pd
import json
from raw_tweets_processor import Processor


processor = Processor()

class TestTweetsProcessor(unittest.TestCase):

    def test_data_loader(self):
        data = json.load(open("../test_resources/test_tweets.json", "r"))
        self.assertEqual(len(data), 20)

    def test_extract_mentions(self):

        tweet = json.load(open("../test_resources/test_tweets.json", "r"))[0]
        expected = "Dr Murphy (DrMurphy11), Babylon (babylonhealth), BadBotThreads (BadBotThreads)"
        actual = processor.extract_mentions(tweet['entities']['user_mentions'])
        self.assertEqual(expected, actual)

    def test_date_formatter(self):
        orig = "Tue Mar 19 11:41:57 +0000 2019"
        expected = "19/03/2019"
        self.assertEqual(expected, processor.get_readable_date(orig))

    def test_extract_all(self):
        all_tweets = json.load(open("../test_resources/test_tweets.json", "r"))[:2]
        full = "@DrMurphy11 @TELUS @babylonhealth @CBCNews @BadBotThreads It will play well in every money-driven " \
               "health insurance market as each \"worried well\" having additional consultations will pay privately " \
               "or an insurer wilk (which then recoups via increased premiums) - makes me so angry."
        mentions = "Dr Murphy (DrMurphy11), TELUS (TELUS), Babylon (babylonhealth), CBC News (CBCNews), " \
                   "BadBotThreads (BadBotThreads)"
        expected = [262, 0, 0, '19/03/2019', full, mentions]
        processed = processor.extract_info(all_tweets)

        t1, t2 = processed.iloc[0], processed.iloc[1]

        actual = [t1['u_followers'], t1['t_retweets'], t1['t_favorited'], t2['t_date'], t2['t_text'], t2['t_mentions']]
        self.assertListEqual(expected, actual)
