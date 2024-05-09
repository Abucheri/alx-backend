#!/usr/bin/env python3
"""
Defines the LRUCache class
"""

BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache class inherits from BaseCaching and implements LRU caching
    algorithm.
    """
    def __init__(self):
        """
        Initializes the LRUCache instance.
        """
        super().__init__()
        self.usage_order = []

    def put(self, key, item):
        """
        Adds an item to the cache using LRU algorithm.

        Args:
            key: The key of the item to be added.
            item: The item to be added to the cache.

        Returns:
            None
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                least_recently_used_key = self.usage_order.pop(0)
                del self.cache_data[least_recently_used_key]
                print("DISCARD:", least_recently_used_key)
            self.cache_data[key] = item
            self.usage_order.append(key)

            # Update usage order by moving the most recently used key
            # to the end
            self.usage_order.remove(key)
            self.usage_order.append(key)

    def get(self, key):
        """
        Retrieves an item from the cache.

        Args:
            key: The key of the item to be retrieved.

        Returns:
            The item associated with the given key, or None if the key is not
            found or is None.
        """
        if key is not None and key in self.cache_data:
            # Update usage order by moving the most recently used key to the
            # end
            self.usage_order.remove(key)
            self.usage_order.append(key)
            return self.cache_data[key]
        return None
