"""
Performance optimization utilities for the meal planner application.
"""

import functools
import time
from typing import Any, Callable, Dict, Optional, TypeVar

from meals.utils.logger import logger

T = TypeVar("T")


# Cache for memoization
_cache: Dict[str, Dict[str, Any]] = {}


def memoize(ttl: int = 60) -> Callable:
    """
    Memoize a function with a time-to-live (TTL) in seconds.
    
    Args:
        ttl: Time-to-live in seconds.
    
    Returns:
        Decorated function.
    """
    def decorator(func: Callable) -> Callable:
        cache_key = f"{func.__module__}.{func.__qualname__}"
        if cache_key not in _cache:
            _cache[cache_key] = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Create a key from the arguments
            key = str(args) + str(sorted(kwargs.items()))
            
            # Check if the result is in the cache and not expired
            if key in _cache[cache_key]:
                result, timestamp = _cache[cache_key][key]
                if time.time() - timestamp < ttl:
                    return result
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            _cache[cache_key][key] = (result, time.time())
            return result
        
        return wrapper
    
    return decorator


def clear_cache(func: Optional[Callable] = None) -> None:
    """
    Clear the cache for a function or all functions.
    
    Args:
        func: Function to clear the cache for. If None, clear all caches.
    """
    if func is None:
        _cache.clear()
    else:
        cache_key = f"{func.__module__}.{func.__qualname__}"
        if cache_key in _cache:
            _cache[cache_key].clear()


def measure_execution_time(func: Callable) -> Callable:
    """
    Measure the execution time of a function.
    
    Args:
        func: Function to measure.
    
    Returns:
        Decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.debug(f"{func.__qualname__} executed in {execution_time:.4f} seconds")
        return result
    
    return wrapper


def lazy_property(func: Callable) -> property:
    """
    Create a lazy property that is computed only once.
    
    Args:
        func: Function to compute the property.
    
    Returns:
        Property descriptor.
    """
    attr_name = f"_{func.__name__}"
    
    @property
    @functools.wraps(func)
    def wrapper(self) -> Any:
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    
    return wrapper