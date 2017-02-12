import os
import json
import click

from twitter import Twitter
from cache import get_last_tweet_id, set_last_tweet_id
from google_nlp import Google
from image_processing import make_image

# Planning to run this once per hour. Doubt he'll spam more than 50 over that
# length of time. ¯\_(ツ)_/¯
TWEET_LIMIT = 50

# Only tweets with a score less than this will be included
ANGER_SCORE_CUTOFF = 0

@click.command()
@click.option('--limit', default=TWEET_LIMIT, help='number of tweets')
@click.option('--nocache', is_flag=True, help='disable using the last cached tweet as a starting point')
@click.option('--nopost', is_flag=True, help='disable posting the images')
def main(limit, nocache, nopost):
    twitter = Twitter()
    google = Google()

    # Check if we already have a tweet id to start from
    last_tweet_id = None if nocache else get_last_tweet_id()

    # Grab any new tweets
    new_tweets = twitter.get_new_trump_tweets(limit=limit,
                                              since_id=last_tweet_id)

    # If there aren't any we're done
    if not new_tweets:
        print("No new tweets since id: {}".format(last_tweet_id))
        return

    # Store the new last_tweet_id. Newest first, so it's just the id of the
    # most recent one.
    set_last_tweet_id(new_tweets[0].id_str)

    # Sentiment analysis
    angry_tweets = []
    for tweet in new_tweets:
        score, mag = google.analyze_text_sentiment(tweet.text)
        if score < ANGER_SCORE_CUTOFF or "SEE YOU IN COURT" in tweet.text:
            angry_tweets.append(tweet)
            # print("\"{}\"\n\t{} / {}".format(tweet.text, score, mag))

    if not angry_tweets:
        print("No new _angry_ tweets since id: {}".format(last_tweet_id))

    for tweet in angry_tweets:
        if nopost:
            print("Tweet: \"{}\"".format(tweet.text))
        else:
            print("Making image for: \"{}\"".format(tweet.text))
            image_path = make_image(tweet.text)
            print("Posting...")
            twitter.post_image(image_path)
            print("Done")

if __name__ == "__main__":
    main()
