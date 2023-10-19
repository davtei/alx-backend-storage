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
        redis_store.incr("count:{}".format(url))
        result = redis_store.get("count:{}".format(url))
        if result:
            return result.decode("utf-8")
        result = method(url)
        redis_store.set("count:{}".format(url), 0)
        redis_store.expire("count:{}".format(url), 10, result)
        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """ Use requests to get the HTML content of a particular URL """
    return requests.get(url).text
