#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """

import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
""" Redis instance """


def data_cacher(method: Callable) -> Callable:
    """ Cache a request with expiration of 10 seconds """
    @wraps(method)
    def wrapper(url):
        """ Wrapper function """
        redis_key = "cached:{}".format(url)
        redis_store.setex(redis_key, 10, "Cached data")
        return method(url)
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """ Use requests to get the HTML content of a particular URL """
    return requests.get(url).text
