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
    def wrapper(self, *args, **kwargs) -> Any:
        """wrapper function to count calls"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Stores history of inputs and outputs"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function"""
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))
        value = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(value))
        return value

    return wrapper


def replay(method: Callable) -> None:
    """Displays history of calls of a particular function"""
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    input_keys = method.__self__._redis.lrange(input_key, 0, -1)
    output_keys = method.__self__._redis.lrange(output_key, 0, -1)

    print("{} was called {} times:".format(
        method.__qualname__, len(input_keys)))
    for inp, out in zip(input_keys, output_keys):
        print(
            "{}(*{}) -> {}".format(
                method.__qualname__, inp.decode("utf-8"), out.decode("utf-8")
            )
        )


class Cache:
    """Class that resembles cache"""

    def __init__(self) -> None:
        """Instantiation when called"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method that stores a value in redis"""
        new_str = str(uuid.uuid4())
        self._redis.set(new_str, data)
        return new_str

    def get(self,
            key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
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
