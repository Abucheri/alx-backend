#!/usr/bin/env python3
"""
Defines the LIFOCache class
"""

BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache class inherits from BaseCaching and implements LIFO caching
    algorithm.
    """
    def __init__(self):
        """
        Initializes the LIFOCache instance.
        """
        super().__init__()
        self.keys_stack = []

    def put(self, key, item):
        """
        Adds an item to the cache using LIFO algorithm.

        Args:
            key: The key of the item to be added.
            item: The item to be added to the cache.

        Returns:
            None
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_key = self.keys_stack.pop()
                del self.cache_data[discarded_key]
                print("DISCARD:", discarded_key)
            self.cache_data[key] = item
            self.keys_stack.append(key)

    def get(self, key):
        """
        Retrieves an item from the cache.

        Args:
            key: The key of the item to be retrieved.

        Returns:
            The item associated with the given key, or None if the key is not
            found or is None.
        """
        if key is not None:
            return self.cache_data.get(key)
        return None
