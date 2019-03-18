from fetcher import TwitterClient
from raw_tweets_processor import Processor
from ugly_analyser import analyse
from utils import get_timestamp
import os
import json
import logging

logging.basicConfig(level="WARN")

LOGGER = logging.Logger("Main")


def create_paths():
    if not os.path.exists("../resources/outputs"):
        os.mkdir("../resources/outputs")


def do_magic(keywords, limit, save):
    create_paths()
    print("Keywords:\n- {}".format("\n- ".join(keywords)))
    print("Trying to extract {} tweets".format(limit))

    # Querying Twitter, saving results to file
    tc = TwitterClient()
    query = " OR ".join(keywords)
    raw_tweets = tc.get_raw_tweets("{} -filter:retweets -from:babylonhealth".format(query), limit)

    raw_tweets_output = "../resources/outputs/raw_tweets_{}.json".format(get_timestamp())
    with open(raw_tweets_output, 'w') as outfile:
        json.dump(raw_tweets, outfile)

    # Reading raw tweets, extracting data into dataframe, saving to csv
    processor = Processor()
    dataframe = processor.extract_info()

    dataframe_output_file = "../resources/outputs/dataframe_results_{}.csv".format(get_timestamp())
    LOGGER.info("Saving dataframe to csv file 'resources/outputs/dataframe_results_{}.csv'".format(get_timestamp()))
    dataframe.to_csv(dataframe_output_file)

    # Producing some numbers with the data
    summary_list = analyse(dataframe)
    LOGGER.info("{} Result summary {}".format("~" * 10, "~" * 10))
    LOGGER.info("\n\t".join(summary_list))


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Analyses tweets to see what people say about Babylon !")
    parser.add_argument("keywords", nargs="*", type=str, help="Keywords to search Twitter", default=['babylonhealth'])
    parser.add_argument("limit", type=int, help="Max number of tweets to fetch", default=100)
    parser.add_argument("save_intermediate", type=bool, action="store_true", default=True)

    args = parser.parse_args()
    print(args)
    do_magic(**vars(args))
