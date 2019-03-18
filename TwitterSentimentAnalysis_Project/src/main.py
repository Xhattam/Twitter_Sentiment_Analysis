from fetcher import TwitterClient
from raw_tweets_processor import Processor
import os


def create_paths():
    if not os.path.exists("../resources/outputs"):
        os.mkdir("../resources/outputs")


def do_magic(keywords, limit, save):
    create_paths()
    print("Keywords:\n- {}".format("\n- ".join(keywords)))
    print("Trying to extract {} tweets".format(limit))

    # Querying Twitter, saving results to file
    tc = TwitterClient()
    q = " OR ".join(keywords)
    tc.get_raw_tweets("{} -filter:retweets -from:babylonhealth".format(q), limit, save)

    # Reading raw tweets, extracting data into dataframe
    processor = Processor(save)
    dataframe = processor.extract_info()



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Analyses tweets to see what people say about Babylon !")
    parser.add_argument("keywords", nargs="*", type=str, help="Keywords to search Twitter", default=['babylonhealth'])
    parser.add_argument("limit", type=int, help="Max number of tweets to fetch", default=100)
    parser.add_argument("save_intermediate", type=bool, action="store_true", default=True)

    args = parser.parse_args()
    print(args)
    do_magic(**vars(args))
