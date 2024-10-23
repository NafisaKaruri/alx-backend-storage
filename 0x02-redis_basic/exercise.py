#!/usr/bin/env python3
"""
Cache class for storing data in Redis.
"""
from typing import Callable, Optional, Union
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

    def get(
            self, key: str, fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """
        Retrieve data from Redis and apply a conversion function if provided.

        Args:
            key (str): The key for the data to retrieve.
            fn (Optional[Callable]): A function to convert the retrieved data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved and
            converted data, or None if the key does not exist.
        """
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        """
        Retrieve a UTF-8 string from Redis.

        Args:
            key (str): The key for the data to retrieve.

        Returns:
            Optional[str]: The retrieved string, or None if key does not exist
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer from Redis.

        Args:
            key (str): The key for the data to retrieve.

        Returns:
            Optional[int]: The retrieved integer, or None if key does not exist
        """
        return self.get(key, lambda x: int(x))
