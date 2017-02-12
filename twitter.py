import os
import re
import html
import tweepy

# Environment Variables
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")

# @realDonaldTrump user id
TRUMP_USER_ID = "25073877"

class Twitter():
    """Twitter wrapper"""

    def __init__(self):
        # Setup Tweepy
        self.auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY,
                                        TWITTER_CONSUMER_SECRET)
        self.auth.set_access_token(TWITTER_ACCESS_TOKEN,
                                   TWITTER_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)


    def get_new_trump_tweets(self, since_id=None, limit=None):
        processed_tweets = []
        for tweet in tweepy.Cursor(self.api.user_timeline,
                                   user_id=TRUMP_USER_ID,
                                   since_id=since_id).items(limit):
            processed = self.process_tweet(tweet)
            if processed:
                processed_tweets.append(processed)
        return processed_tweets

    def process_tweet(self, tweet):
        # Don't want retweets. Only angry messages from Easy D.
        if tweet.retweeted:
            return None

        # Unescape HTML entities
        tweet.text = html.unescape(tweet.text)

        # Remove URLS
        tweet.text = re.sub(r"http\S+", "", tweet.text)

        # Remove extra characters and whitespace
        tweet.text = tweet.text.replace("\n", "")
        tweet.text = tweet.text.replace("\r", "")
        tweet.text = tweet.text.strip()
        return tweet

    def post_image(self, image_path):
        try:
            # Returns the tweet
            return self.api.update_with_media(image_path)
        except TweepError as e:
            print("Error: {}".format(e.message))
        return None
