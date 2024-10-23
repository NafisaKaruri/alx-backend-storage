#!/usr/bin/env python3
"""
Cache class for storing data in Redis.
"""
from typing import Union
import redis
import uuid


class Cache:
    """
    A simple cache class using Redis.
    """
    def __init__(self) -> None:
        """
        Initialize the Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the generated key.

        Args:
            data(Union[str, bytes, int, float]): The data to store in the cache

        Returns:
            str: The key under which the data is stored.
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key
