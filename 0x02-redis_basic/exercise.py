#!/usr/bin/env python3
"""
Cache class for storing data in Redis.
"""
from functools import wraps
from typing import Any, Callable, Union
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with call counting.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Increment the call count in Redis and call the original method.

        Args:
            self: The instance of the class.
            *args: Positional arguments for the original method.
            **kwargs: Keyword arguments for the original method.

        Returns:
            The result of the original method call.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with call history.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls for a specific Cache method.

    Args:
        method (Callable): The method for which to replay the history.
    """
    if method is None or not hasattr(method, '__self__'):
        return

    redis_client = getattr(method.__self__, '_redis', None)
    if not isinstance(redis_client, redis.Redis):
        return

    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"
    call_no = int(redis_client.get(method.__qualname__) or 0)
    print(f'{method.__qualname__} was called {call_no} times:')

    input_history = redis_client.lrange(input_key, 0, -1)
    output_history = redis_client.lrange(output_key, 0, -1)

    for input_value, output_value in zip(input_history, output_history):
        print('{}(*{}) -> {}'.format(
            method.__qualname__,
            input_value.decode('utf-8'),
            output_value.decode('utf-8'),
        ))


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

    @count_calls
    @call_history
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
