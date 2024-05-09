#!/usr/bin/env python3
"""
Defines the MRUCache class
"""

from collections import OrderedDict

BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache class inherits from BaseCaching and implements MRU caching
    algorithm.
    """
    def __init__(self):
        """
        Initializes the MRUCache instance.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Adds an item to the cache using MRU algorithm.

        Args:
            key: The key of the item to be added.
            item: The item to be added to the cache.

        Returns:
            None
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                most_recently_used_key = next(reversed(self.cache_data))
                del self.cache_data[most_recently_used_key]
                print("DISCARD:", most_recently_used_key)
            self.cache_data[key] = item

    def get(self, key):
        """
        Retrieves an item from the cache.

        Args:
            key: The key of the item to be retrieved.

        returns:
            The item associated with the given key, or None if the key is not
            found or is None.
        """
        if key is not None and key in self.cache_data:
            # Move the accessed item to the end to maintain MRU order
            value = self.cache_data.pop(key)
            self.cache_data[key] = value
            return value
        return None
