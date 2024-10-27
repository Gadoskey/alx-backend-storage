#!/usr/bin/env python3
"""
Author: Gadoskey
File: exercise.py
Description: A Python class that writes and retrieves strings to/from Redis
"""
from typing import Callable, Optional, Union
from functools import wraps
from uuid import uuid4
import redis


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__  # Get the qualified name of the method
        self._redis.incr(key)  # Increment the call count in Redis
        return method(self, *args, **kwargs)  # Call the original method
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Input and output keys for storing in Redis
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        
        # Log input parameters by appending to the inputs list
        self._redis.rpush(input_key, str(args))
        
        # Execute the original method and log the output
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        
        return output
    return wrapper

def replay(method: Callable):
    """
    Display the history of calls of a particular function.
    """
    # Get the qualified name for the input and output keys
    redis_instance = method.__self__._redis
    method_name = method.__qualname__
    
    # Fetch input and output logs from Redis
    inputs = redis_instance.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{method_name}:outputs", 0, -1)
    
    # Display the number of calls and each call’s details
    print(f"{method_name} was called {len(inputs)} times:")
    for input_args, output in zip(inputs, outputs):
        print(f"{method_name}(*{input_args.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    def __init__(self):
        # Initializing Cache with Redis instance
        self._redis = redis.Redis()
        self._redis.flushdb()
        
    @count_calls
    @call_history
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
        data = self.get(key)  # Get the raw data from Redis
        if data is not None:
            decoded_data = data.decode("utf-8")  # Decode str to a UTF-8 string
            return decoded_data
        return None

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves data from Redis and converts it to an integer.
        """
        data = self.get(key)  # Get the raw data from Redis
        if data is not None:
            int_data = int(data)  # Convert str to an integer
            return int_data
        return None
