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
