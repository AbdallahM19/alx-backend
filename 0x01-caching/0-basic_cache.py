#!/usr/bin/python3
"""cache system"""

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """a class BasicCache that inherits from BaseCaching"""
    def __init__(self):
        """init method"""
        super().__init__()

    def put(self, key, item):
        """add an item to the cache"""
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """get an item from the cache"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
