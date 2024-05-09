#!/usr/bin/env python3
"""
Defines the LFUCache class
This LFU caching algorithm ensures that when the cache is full and a new item
needs to be added, it removes the least frequently used item. If there are
multiple least frequently used items, it removes the least recently used among
them.
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
        It first checks if both key and item are not None.
        If the cache is full (the number of items exceeds
        BaseCaching.MAX_ITEMS), it finds the least frequently used key(s)
        by finding the minimum frequency from self.keys_freqs. If there are
        multiple keys with the same minimum frequency, it selects the one
        that was least recently used (LRU) based on the order in
        self.cache_data. It then deletes the least recently used key from
        both self.cache_data and self.keys_freqs. After that, it adds the
        new key and item to self.cache_data and sets its frequency to 1 in
        self.keys_freqs.

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
                least_recently_used_key = min(least_freq_keys,
                                              key=lambda k: self.cache_data[k])
                del self.cache_data[least_recently_used_key]
                del self.keys_freqs[least_recently_used_key]
                print("DISCARD:", least_recently_used_key)
            self.cache_data[key] = item
            self.keys_freqs[key] = 1

    def get(self, key):
        """
        Retrieves an item from the cache.
        It checks if key is not None and exists in self.cache_data.
        If the key exists, it increments its frequency in self.keys_freqs
        and returns the corresponding item from self.cache_data. If the key
        doesn't exist or is None, it returns None.

        Args:
            key: The key of the item to be retrieved.

        Returns:
            The item associated with the given key, or None if the key is not
            found or is None.
        """
        if key is not None and key in self.cache_data:
            self.keys_freqs[key] += 1
            return self.cache_data[key]
        return None
