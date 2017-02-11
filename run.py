import os
import json

from twitter import Twitter
from google_nlp import Google
from cache import get_last_tweet_id, set_last_tweet_id

# Planning to run this once per hour. Doubt he'll spam more than 50 over that
# length of time. ¯\_(ツ)_/¯
TWEET_LIMIT = 50

def main():
    twitter = Twitter()
    google = Google()

    # Check if we already have a tweet id to start from
    last_tweet_id = get_last_tweet_id()

    # Grab any new tweets
    new_tweets = twitter.get_new_trump_tweets(limit=TWEET_LIMIT,
                                              since_id=last_tweet_id)

    # If there aren't any we're done
    if not new_tweets:
        print("No new tweets since id:{}".format(last_tweet_id))
        return

    # Store the new last_tweet_id. Newest first, so it's just the id of the
    # most recent one.
    set_last_tweet_id(new_tweets[0].id)

    for tweet in new_tweets:
        score, mag = google.analyze_text_sentiment(tweet.text)
        print("\"{}\"\n\t{} / {}".format(tweet.text, score, mag))

if __name__ == "__main__":
    main()
