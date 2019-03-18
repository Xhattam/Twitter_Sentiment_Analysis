import pandas as pd
import sys
import logging

logging.basicConfig(level="WARN")


class UglyAnalyser:

    def __init__(self, data, save):
        if not data:
            try:
                self.df = pd.read_csv("../resources/outputs/dataframe_results.csv")
            except FileNotFoundError as e:
                sys.exit(e)
        else:
            self.df = data
        self.logger = logging.Logger(name="UglyAnalyser")
        self.save = save

    def analyse(self):
        """ Extracts some insight from the data, writes the results in text format """

        result_output = []

        dates = self.df['t_date'].unique()
        dates.sort()
        range_dates = dates[0] + " - " + dates[-1]

        most_active_overall = self.df['u_screen_name'].mode()[0]
        most_neg_user = self.df.loc[self.df['t_polarity'] == "Negative"].groupby(['u_screen_name']).size().idxmax()
        most_pos_user = self.df.loc[self.df['t_polarity'] == 'Positive'].groupby(['u_screen_name']).size().idxmax()
        most_neg_tweet = self.df.iloc[self.df['t_polarity_score'].idxmin()]

        most_pos_tweet = self.df.iloc[self.df['t_polarity_score'].idxmax()]
        avg_neg_polarity = self.df.loc[self.df['t_polarity'] == 'Negative']['t_polarity_score'].mean()
        avg_pos_polarity = self.df.loc[self.df['t_polarity'] == "Positive"]['t_polarity_score'].mean()
        percentages = self.df['t_polarity'].value_counts(normalize=True) * 100

        result_output.append("Time frame: {}\n".format(range_dates))
        result_output.append("Most active user: {}\n".format(most_active_overall))
        result_output.append("User with most negative tweets: {}\n".format(most_neg_user))
        result_output.append("User with most positive tweets: {}\n".format(most_pos_user))
        result_output.append("Most negative tweet")
        result_output.append(most_neg_tweet[['t_polarity_score', 't_polarity', 'u_screen_name']])
        result_output.append("Tweet: {}\n".format(most_neg_tweet['t_text']))
        result_output.append("Most positive tweet")
        result_output.append(most_pos_tweet[['t_polarity_score', 't_polarity', 'u_screen_name']])
        result_output.append("Tweet: {}\n".format(most_pos_tweet['t_text']))
        result_output.append("Percentages of tweets by polarity")
        result_output.append(percentages)
        result_output.append("Average negative polarity: {}\n".format(avg_neg_polarity))
        result_output.append("Average positive polarity: {}\n".format(avg_pos_polarity))

        print("\n\t".join(result_output))