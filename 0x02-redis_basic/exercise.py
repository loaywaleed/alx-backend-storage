#!/usr/bin/env python3
"""
Redis Moduel
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Any


def count_calls(method: Callable) -> Callable:
    """Number of calls made to a method"""

    @wraps(method)
    def wrapper(self, args, **kwargs) -> Any:
        """wrapper function to count calls"""
        if isinstance(self._redis, redis.Redis) == True:
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Class that resembles cache"""

    def __init__(self) -> None:
        """Instantiation when called"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method that stores a value in redis"""
        new_str = str(uuid.uuid4())
        self._redis.set(new_str, data)
        return new_str

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """getting value given a key"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Conversion to string"""
        return self.get(key,  fn=str)

    def get_int(self, key: str) -> int:
        """Conversion to int"""
        return self.get(key, fn=int)
