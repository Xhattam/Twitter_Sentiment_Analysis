import seaborn as sns
import matplotlib.pyplot as plt
import logging
from os.path import abspath
from utils import get_timestamp
import webbrowser
sns.set_style("dark", {'axes.grid': True})


""" Show results in a pretty, graphic way

@author: Jessica Tanon

DATE: MARCH 2019
"""


logging.basicConfig(level="INFO")


class PrettyAnalyser:

    """ Analyses dataframe from Processor, and builds charts on the following numbers:
        - most active user with negative tweets (bar chart)
        - most active user with positive tweets (bar chart)
        - most active user (bar chart)
        - percentage of positive/neutral/negative tweets (pie chart)
    """

    def __init__(self):
        self._logger = logging.Logger(name="PrettyAnalyser")

    def make_plots(self, df):
        """ Calls all plot functions

        :param df   : input dataframe
        :type df    : pandas.DataFrame
        """
        self.plot_most_polarity_user(df, 'Negative')
        self.plot_most_polarity_user(df, 'Positive')
        self.plot_most_active_users(df)
        self.polarity_ratio_chart(df)
        self.show_best_worst_tweet(df)

    def horiz_plot(self, data, x, y, palette, xlim_upper, max_values, figsize, title, output_name):
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
        plt.suptitle(title)
        barplot = sns.barplot(x=x, y=y, data=data, palette=palette)

        ax.legend(ncol=1, loc="lower right", frameon=True)
        ax.set(xlim=(0, xlim_upper), xlabel="Number of tweets", ylabel="")
        sns.despine(left=True, bottom=True)
        self._logger.info("Saving figure to {}".format(abspath("../outputs/{}".format(output_name))))
        barplot.get_figure().savefig("../outputs/{}".format(output_name))

    def plot_most_polarity_user(self, df, polarity):
        """ Plots the most positive/negative 20 users

        :param df       : input dataframe
        :type df        : pandas.DataFrame
        :param polarity : value of polarity to look at (Positive, Negative, Neutral)
        :type polarity  : str
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
            palette=palette,
            xlim_upper=max(sorted_users['t_polarity'])+1,
            max_values=20,
            figsize=(15, 25),
            title="Users with the most {} tweets (top 20 users)".format(polarity.lower()),
            output_name="20_users_most_{}_tweets_{}.png".format(polarity.lower(), get_timestamp()))

    def plot_most_active_users(self, df):
        """ Plots user activity, counted in tweets written

        :param df   : input dataframe
        :type df    : pandas.DataFrame
        """
        # creating new dataframe with user and tweet counts as columns
        users = df['u_screen_name'].value_counts().rename_axis('u_screen_name').reset_index(name='tweets')
        show_n_users = 50
        palette = sns.cubehelix_palette(show_n_users, reverse=True, light=0.8, dark=0.1)
        self.horiz_plot(data=users, x="tweets", y="u_screen_name", palette=palette,
                        xlim_upper=max(users['tweets'])+1, max_values=show_n_users, figsize=(15, 25),
                        title="Number of tweets per user (50 users)",
                        output_name="most_active_50_users_per_number_of_tweets_{}".format(get_timestamp()))

    def polarity_ratio_chart(self, df):
        """ Creates pie chat of positive/negative/neutral polarity ratios

        :param df   : input dataframe
        :type df    : pandas.DataFrame
        """
        labels = ["Positive", "Neutral", "Negative"]
        pos = df.loc[df['t_polarity'] == 'Positive']
        neg = df.loc[df['t_polarity'] == 'Negative']
        neu = df.loc[df['t_polarity'] == 'Neutral']
        sizes = [len(pos), len(neu), len(neg)]
        cols = ['g', 'lavender', 'r']

        fig1, ax1 = plt.subplots()
        plt.suptitle("Tweets polarity ratio")
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, colors=cols)
        ax1.axis('equal')
        plt.show()

    def show_best_worst_tweet(self, df):
        """ Display tweet with best/worst polarity in a browser

        :param df   : input dataframe
        :type df    : pandas.DataFrame
        """

        def open_link(link):
            """ Tries to open twitter link, and logs warning if there's an error
            :param link : url to open
            :type link  : str"""
            try:
                webbrowser.open(link)
            except:
                self._logger.warn("Couldn't open link at {}".format(link))

        # twitter base link to a tweet
        base_link = "http://twitter.com/{}/status/{}"

        # Worst tweet author, id and twitter link
        worst = df.iloc[df['t_polarity_score'].idxmin()]
        worst_user = worst['u_screen_name']
        worst_id = worst['t_id']
        worst_link = base_link.format(worst_user, worst_id)

        # Best tweet author, id and twitter link
        best = df.iloc[df['t_polarity_score'].idxmax()]
        best_user = best['u_screen_name']
        best_id = best['t_id']
        best_link = base_link.format(best_user, best_id)

        open_link(worst_link)
        open_link(best_link)








