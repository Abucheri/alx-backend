#!/usr/bin/env python3
"""
Defines the FIFOCache class
"""

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache class inherits from BaseCaching and implements FIFO caching
    algorithm.
    """
    def __init__(self):
        """
        Initializes the FIFOCache instance.
        """
        super().__init__()
        self.keys_queue = []

    def put(self, key, item):
        """
        Adds an item to the cache using FIFO algorithm.

        Args:
            key: The key of the item to be added.
            item: The item to be added to the cache.

        Returns:
            None
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_key = self.keys_queue.pop(0)
                del self.cache_data[discarded_key]
                print("DISCARD:", discarded_key)
            self.cache_data[key] = item
            self.keys_queue.append(key)

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
