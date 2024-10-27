#!/usr/bin/env python3
""" Redis Module for Caching and Counting URL Requests """

from functools import wraps
import redis
import requests
from typing import Callable

# Initialize Redis connection
redis = redis.Redis()

def count_requests(method: Callable) -> Callable:
    """Decorator to count URL requests and cache HTML content."""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper for the decorated function."""
        
        # Increment the request count for the given URL
        redis.incr(f"count:{url}")
        
        # Check if the HTML content for the URL is already cached
        cached_html = redis.get(f"cached:{url}")
        
        # If cached, return the cached content
        if cached_html:
            return cached_html.decode('utf-8')
        
        # Otherwise, fetch the HTML, cache it, and return the content
        html = method(url)
        redis.setex(f"cached:{url}", 10, html)  # Cache expires in 10 seconds
        return html

    return wrapper

@count_requests
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL."""
    response = requests.get(url)
    return response.text
