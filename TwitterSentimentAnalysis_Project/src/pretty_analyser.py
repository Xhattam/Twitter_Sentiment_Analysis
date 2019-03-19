""" Show results in a pretty, graphic way

@author: Jessica Tanon

DATE: MARCH 2019
"""

import seaborn as sns
sns.set_style("dark", {'axes.grid': True})
import matplotlib.pyplot as plt
import logging
from os.path import abspath
from utils import get_timestamp

logging.basicConfig(level="WARN")


class PrettyAnalyser:

    def __init__(self):
        self._logger = logging.Logger(name="PrettyAnalyser")

    def make_plots(self, df):
        self.plot_most_polarity_user(df, 'Negative')
        self.plot_most_polarity_user(df, 'Positive')
        self.plot_most_active_users(df)
        self.polarity_ratio_chart(df)

    def horiz_plot(self, data, x, y, label, palette, xlim_upper, max_values, figsize, title, output_name):
        """ Horizontal bar plot

        :param data         : dataframe with sorted/counted columns of interest
        :type data          : pandas.DataFrame
        :param x            : column name to use for data on x axis
        :type x             : str
        :param y            : column name to use for data on y axis
        :type y             : str
        :param label        : plot label for bars
        :type label         : str
        :param palette      : colour palette to use for bars
        :type palette       : list of str, or seaborn palette pobject
        :param xlim_upper   : max value to use on x axis
        :type xlim_upper    : int
        :param max_values   : number of rows to use from dataframe
        :type max_values    : int
        ;param figsize      : size of figure
        :type figsize       : tuple of ints
        :param title        : title
        :type title         : str
        :param output_name  : name to use for output file
        :type output_name   : str
        """
        f, ax = plt.subplots(figsize=figsize)
        data = data.head(max_values)

        barplot = sns.barplot(x=x, y=y, data=data, label=label, palette=palette)

        ax.legend(ncol=1, loc="lower right", frameon=True)
        ax.set(xlim=(0, xlim_upper), ylabel="", xlabel=title)
        sns.despine(left=True, bottom=True)
        self._logger.info("Saving figure to {}".format(abspath("../outputs/{}".format(output_name))))
        barplot.get_figure().savefig("../outputs/{}".format(output_name))

    def plot_most_polarity_user(self, df, polarity):
        """ Plots the most positive/negative 20 users

        :param polarity: value of polarity to look at (Positive, Negative, Neutral)
        :return:
        """
        neg_polarity_df = df.loc[df['t_polarity'] == polarity][['u_screen_name', 't_polarity']]
        sorted_users = neg_polarity_df.groupby('u_screen_name').count().sort_values(
            by="t_polarity", ascending=False)
        sorted_users.reset_index(level=0, inplace=True)
        if len(sorted_users['t_polarity'].unique()) == 1:
            palette = ['silver' for x in sorted_users['t_polarity']]
        else:
            palette = ['silver' if (x < max(sorted_users['t_polarity'])) else 'red' for x in sorted_users['t_polarity']]

        self.horiz_plot(
            data=sorted_users,
            x="t_polarity",
            y="u_screen_name",
            label="#tweets",
            palette=palette,
            xlim_upper=max(sorted_users['t_polarity'])+1,
            max_values=20,
            figsize=(6, 15),
            title="Top 20 users with the most {} tweets".format(polarity.lower()),
            output_name="20_users_most_{}_tweets_{}.png".format(polarity.lower(), get_timestamp()))

    def plot_most_active_users(self, df):
        """ Plots user activity, counted in tweets written

        :param df: data to look at
        :type df: pandas.DataFrame
        """
        # creating new dataframe with user and tweet counts as columns
        users = df['u_screen_name'].value_counts().rename_axis('u_screen_name').reset_index(name='tweets')
        palette = sns.cubehelix_palette(len(users), reverse=True, light=0.8, dark=0.1)
        self.horiz_plot(data=users, x="tweets", y="u_screen_name", label="#tweets", palette=palette,
                        xlim_upper=max(users['tweets'])+1, max_values=50, figsize=(15, 25),
                        title="Number of tweets per user (50 users)",
                        output_name="most_active_50_users_per_number_of_tweets_{}".format(get_timestamp()))


    def polarity_ratio_chart(self, df):
        labels = ["Positive", "Neutral", "Negative"]
        pos = df.loc[df['t_polarity'] == 'Positive']
        neg = df.loc[df['t_polarity'] == 'Negative']
        neu = df.loc[df['t_polarity'] == 'Neutral']
        sizes = [len(pos), len(neu), len(neg)]
        cols = ['g', 'white', 'r']

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, colors=cols)
        ax1.axis('equal')
        ax1.legend(ncol=1, loc="lower right", frameon=True)
        plt.show()







