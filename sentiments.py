import os

import tweepy, re
from textblob import TextBlob
from flask import Blueprint, render_template, request

second = Blueprint("second", __name__, static_folder="static", template_folder="template")


@second.route("/sentiment_analyzer")
def sentiment_analyzer():
    return render_template("sentiment_analyzer.html")


class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self, keyword, tweets):

        # authenticating
        consumerKey = '2uGom8U6ePuf3ikYg5J01beML'
        consumerSecret = 'VrLm3pcfvdxurSOO3PHO1ffgDkBKA42u3WNWcylvCHqww2Vj3E'
        accessToken = '1597280026831261697-j7OZSr5MNAJqQw0JgRrnWVs3zMJYe8'
        accessTokenSecret = 'StzV14YbLeREsN1ClL0ZeOJyefqOrbbZbRtlvhEbFcBBf'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        tweets = int(tweets)

        self.tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang="en").items(tweets)

        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0

        for tweet in self.tweets:
            analysis = TextBlob(self.cleanTweet(tweet.text))
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1

        # finding average of how people are reacting
        positive = self.percentage(positive, tweets)
        wpositive = self.percentage(wpositive, tweets)
        spositive = self.percentage(spositive, tweets)
        negative = self.percentage(negative, tweets)
        wnegative = self.percentage(wnegative, tweets)
        snegative = self.percentage(snegative, tweets)
        neutral = self.percentage(neutral, tweets)

        # finding average reaction
        polarity = polarity / tweets

        if (polarity == 0):
            htmlpolarity = "Neutral"

        elif (polarity > 0 and polarity <= 0.3):
            htmlpolarity = "Weakly Positive"
        elif (polarity > 0.3 and polarity <= 0.6):
            htmlpolarity = "Positive"
        elif (polarity > 0.6 and polarity <= 1):
            htmlpolarity = "Strongly Positive"
        elif (polarity > -0.3 and polarity <= 0):
            htmlpolarity = "Weakly Negative"
        elif (polarity > -0.6 and polarity <= -0.3):
            htmlpolarity = "Negative"
        elif (polarity > -1 and polarity <= -0.6):
            htmlpolarity = "strongly Negative"

        print(polarity,htmlpolarity)
        return polarity,htmlpolarity,positive,wpositive, spositive,negative,wnegative, snegative,neutral,keyword,tweets

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')


@second.route('/sentiment_logic', methods=['POST','GET'])
def sentiment_logic():
    keyword = request.form.get('keyword')
    tweets = request.form.get('tweets')
    sa = SentimentAnalysis()
    polarity,htmlpolarity,positive,wpositive, spositive,negative,wnegative, snegative,neutral,keyword1,tweet1=sa.DownloadData(keyword,tweets)
    return render_template('sentiment_analyzer.html',polarity=polarity,htmlpolarity=htmlpolarity, positive=positive,wpositive=wpositive, spositive=spositive,
                           negative=negative,wnegative=wnegative, snegative=snegative,neutral=neutral,keyword=keyword1,tweets=tweet1)





