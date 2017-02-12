from iron_cache import *

cache = IronCache()


def get_last_tweet_id():
    try:
        item = cache.get(cache="main", key="last_tweet_id")
    except:
        return None
    return item.value

def set_last_tweet_id(id):
    cache.put(cache="main", key="last_tweet_id", value=id)
