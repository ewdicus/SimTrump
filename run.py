import os
import json
from twitter import Twitter

def main():
    twitter = Twitter()
    new_tweets = twitter.get_new_trump_tweets(limit=10)
    for tweet in new_tweets:
        print("\"{}\"".format(tweet.text))

if __name__ == "__main__":
    main()
