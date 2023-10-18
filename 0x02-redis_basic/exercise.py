#!/usr/bin/env python3
""" Writing strings to Redis """

import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """ A Cache class """
    def __init__(self) -> None:
        """ Constructor """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generate a random key, store input data in Redis using the
        random key and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
