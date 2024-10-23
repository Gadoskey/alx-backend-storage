#!/usr/bin/env python3
"""
Author: Gadoskey
File: exercise.py
Description: A Python class that write strings to Redis
"""


class Cache:
  # Class Cache
  def __init__(self):
    # Initializng Class Cache
    self._redis = redis.Redis()
    self._redis.flushdb()
    
  def store(self, data: Union[str, bytes, int, float]) -> str:
    # A store method that takes a data argument and returns a string
    key = str(uuid4())
    self._redis.set(key, data)
    return key
