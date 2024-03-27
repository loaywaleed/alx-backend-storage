#!/usr/bin/env python3
import redis
import uuid
from typing import Union


class Cache:
    """Class that resembles cache"""
    def __init__(self):
        """Instantiation when called"""
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    def store(self, data: Union[str, float, bytes, int]) -> str:
        """Method that stores a value in redis"""
        new_str = str(uuid.uuid4())
        self._redis.set(new_str, data)
        return new_str

        