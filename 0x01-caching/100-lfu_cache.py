#!/usr/bin/env python3
"""
Defines the LFUCache class
"""

from collections import OrderedDict

BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache class inherits from BaseCaching and implements LFU caching
    algorithm.
    """
    def __init__(self):
        """
        Initializes the LFUCache instance.
        """
        super().__init__()
        self.cache_data = OrderedDict()
        self.keys_freqs = {}

    def put(self, key, item):
        """
        Adds an item to the cache using LFU algorithm.

        Args:
            key: The key of the item to be added.
            item: The item to be added to the cache.

        Returns:
            None
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                least_freqs = min(self.keys_freqs.values())
                least_freq_keys = [k for k, v in self.keys_freqs.items()
                                   if v == least_freqs]
                if len(least_freq_keys) > 1:
                    least_recently_used_key = next(iter(self.cache_data))
                    del self.cache_data[least_recently_used_key]
                    del self.keys_freqs[least_recently_used_key]
                    print("DISCARD:", least_recently_used_key)
                else:
                    del self.cache_data[least_freq_keys[0]]
                    del self.keys_freqs[least_freq_keys[0]]
                    print("DISCARD:", least_freq_keys[0])
            self.cache_data[key] = item
            self.keys_freqs[key] = 1

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
            if key in self.cache_data:
                self.keys_freqs[key] += 1
                return self.cache_data[key]
        return None
