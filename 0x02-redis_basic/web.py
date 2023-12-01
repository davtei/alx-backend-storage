#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """

from functools import wraps
from typing import Callable

import redis
import requests


redis_store = redis.Redis()
""" Redis instance """


def data_cacher(method: Callable) -> Callable:
    """ Cache a request with expiration of 10 seconds """
    @wraps(method)
    def wrapper(url) -> str:
        """ Wrapper function """
        redis_store.incr(f"count:{url}", 1)
        result = redis_store.get(f"result:{url}")
        if result:
            return result.decode("utf-8")
        result = method(url)
        redis_store.set(f"count:{url}", 0)
        redis_store.setex(f"result:{url}", 10, result)
        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """ Use requests to get the HTML content of a particular URL """
    return requests.get(url, timeout=30).text
