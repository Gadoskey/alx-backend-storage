#!/usr/bin/env python3
"""
File: web.py
Description: A Python script that retrieves a web page,
caches it, and tracks access count.
"""
import requests
import redis
from functools import wraps
from typing import Callable

# Connect to Redis
cache = redis.Redis()

def count_requests(method: Callable) -> Callable:
    """Decorator to count how many times a URL
    was accessed and cache the page content."""
    @wraps(method)
    def wrapper(url: str) -> str:
        # Increment the count for this URL
        count_key = f"count:{url}"
        cache.incr(count_key)

        # Check if the page content is cached
        cached_content = cache.get(url)
        if cached_content:
            return cached_content.decode("utf-8")

        # If not cached, retrieve from the URL
        content = method(url)

        # Cache the content with a 10-second expiration
        cache.setex(url, 10, content)
        return content
    return wrapper

@count_requests
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL."""
    response = requests.get(url)
    return response.text
