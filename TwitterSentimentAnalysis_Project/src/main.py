from fetcher import TwitterClient
from raw_tweets_processor import Processor
from utils import get_timestamp
import os
import json
import logging
from pretty_analyser import PrettyAnalyser

logging.basicConfig(level=logging.INFO)

LOGGER = logging.Logger("Main")


def create_paths():
    """ Creates `outputs` folder if it doesn't exist """
    if not os.path.exists("../outputs"):
        os.mkdir("../outputs")


def do_magic(keywords, limit):
    """ Main function, does all the heavy lifting (query twitter, processes, analysis, plots)

    :param keywords : keywords to query twitter with
    :type keywords  : list of str
    :param limit    : max number of tweets to get
    :type limit     : int
    """

    # TODO fix stupid logger which doesn't log anything (y tho)
    create_paths()
    print("Keywords:\n- {}".format("\n- ".join(keywords)))
    print("Trying to extract {} tweets".format(limit))

    # Querying Twitter, saving results to file
    tc = TwitterClient()
    query = " OR ".join(keywords)
    raw_tweets = tc.get_raw_tweets("{} -filter:retweets -from:babylonhealth".format(query), limit)

    LOGGER.info("Fetched {}/{} tweets".format(len(raw_tweets), limit))

    raw_tweets_output = "../outputs/raw_tweets_{}.json".format(get_timestamp())
    with open(raw_tweets_output, 'w') as outfile:
        json.dump(raw_tweets, outfile)

    # Reading raw tweets, extracting data into dataframe, saving to csv
    processor = Processor()
    dataframe = processor.extract_info(raw_tweets)
    print("Found {}/{} tweets".format(len(dataframe), limit))

    dataframe_output_file = "../outputs/dataframe_results_{}.csv".format(get_timestamp())
    LOGGER.info("Saving dataframe to csv file '../outputs/dataframe_results_{}.csv'".format(get_timestamp()))
    dataframe.to_csv(dataframe_output_file)

    LOGGER.info("Building plots...")
    analyser = PrettyAnalyser()
    analyser.make_plots(dataframe)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Analyses tweets to see what people say about Babylon !")
    parser.add_argument("keywords", nargs="*", type=str, help="Keywords to search Twitter", default=['babylonhealth'])
    parser.add_argument("-limit", type=int, help="Max number of tweets to fetch", default=100)

    args = parser.parse_args()
    do_magic(**vars(args))
