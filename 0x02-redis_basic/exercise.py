#!/usr/bin/env python3
"""
Author: Gadoskey
File: exercise.py
Description: A Python class that writes and retrieves strings to/from Redis
"""
from typing import Callable, Optional, Union
from uuid import uuid4
import redis


class Cache:
    def __init__(self):
        # Initializing Cache with Redis instance
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis and returns a unique key.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves data from Redis and optionally applies a callable to transform it.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves data from Redis and decodes it to a string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves data from Redis and converts it to an integer.
        """
        return self.get(key, fn=int)
