#!/usr/bin/env python3
"""
Author: Gadoskey
File: exercise.py
Description: A Python class that write strings to Redis
"""
from typing import Callable, Optional, Union
from uuid import uuid4
import redis


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
  
  def get(self, key: str, fn: Optional[Callable]) -> Union[str, bytes, int, float]:
    """ A get method that takes a key string argument and
    an optional Callable argument named fn. It converts data
    back to the desired format
    """
    value = self._redis.get(key)
    if fn:
      value = fn(value)
    return value
  
  def get_str(self, key: str) -> str:
        """
        Automatically parametrizes Cache.get with the correct string function.
        """
        value = self._redis.get(key)
        return value.decode('utf-8')

  def get_int(self, key: str) -> int:
      """
      Automatically parametrizes Cache.get with the correct int function.
      """
      value = self._redis.get(key)
      try:
          value = int(value.decode('utf-8'))
      except Exception:
          value = 0
      return value
