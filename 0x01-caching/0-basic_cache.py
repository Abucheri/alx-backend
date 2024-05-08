#!/usr/bin/env python3
"""Defines the BasicCache class"""

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache class inherits from BaseCaching and implements a basic caching
    system.

    Attributes:
        cache_data (dict): A dictionary to store cached items.
    """
    def put(self, key, item):
        """
        Add an item to the cache.

        Args:
            key: The key of the item to be added.
            item: The item to be added to the cache.

        Returns:
            None

        Notes:
            If either key or item is None, the method does nothing.
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
        Retrieve an item from the cache.

        Args:
            key: The key of the item to be retrieved.

        Returns:
            The item associated with the given key, or None if the key is not
            found or is None.
        """
        if key is not None:
            return self.cache_data.get(key)
        return None
