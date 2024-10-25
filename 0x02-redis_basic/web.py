#!/usr/bin/env python3
"""
Web cache and tracker using Redis.
"""
import redis
import requests
from functools import wraps
from typing import Callable

redis_client = redis.Redis()
"""The Redis instance of the module"""


def cache_page(method: Callable) -> Callable:
    """
    Decorator to cache the results of a method based on the URL.

    Args:
        method (Callable): The method to cache.

    Returns:
        Callable: The wrapped function with caching behavior.
    """
    @wraps(method)
    def invoker(url) -> str:
        """
        Invokes the method and caches the result.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the page or a message.
        """
        # Increment the count for each call
        redis_client.incr(f'count:{url}')

        cached_result = redis_client.get(f'result:{url}')
        if cached_result:
            return cached_result.decode('utf-8')

        # Fetch the page content
        try:
            result = method(url)
            # Cache the result with expiration
            redis_client.setex(f'result:{url}', 10, result)
            return "OK"  # Return OK when fetched and cached
        except Exception as e:
            return "Error fetching page"  # Handle errors gracefully

    return invoker


@cache_page
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The URL of the page to retrieve.

    Returns:
        str: The HTML content of the page.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text
