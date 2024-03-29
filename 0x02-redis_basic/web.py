#!/usr/bin/env python3
'''
A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


_redis = redis.Redis()


def data_cache(method: Callable) -> Callable:
    '''Caches response data'''
    @wraps(method)
    def wrapper(url) -> str:
        '''The wrapper function'''
        _redis.incr(f'count:{url}')
        result = _redis.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        _redis.set(f'count:{url}', 0)
        _redis.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@data_cache
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request'''
    return requests.get(url).text
