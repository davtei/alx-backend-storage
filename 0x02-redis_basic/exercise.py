#!/usr/bin/env python3
""" Writing strings to Redis """

import re
import redis
import uuid
from typing import Union, Callable


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

    def get(
            self, key: str, fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """ Convert data back to desired format """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """ Convert data to string """
        data = self._redis.get(key)
        return data.decode('utf-8')

    def get_int(self, key: str) -> int:
        """ Convert data to int """
        data = self._redis.get(key)
        try:
            return int(data.decode('utf-8'))
        except Exception:
            return 0
