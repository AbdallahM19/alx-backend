#!/usr/bin/python3
"""cache system"""

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """a class FIFOCache that inherits from BaseCaching"""
    def __init__(self):
        """init method"""
        super().__init__()
        self.capacity = BaseCaching.MAX_ITEMS
        self.queue = []

    def get(self, key):
        """get an item from the cache"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)

    def put(self, key, item):
        """add an item to the cache"""
        if key is None or item is None:
            return

        if key not in self.cache_data:
            if len(self.cache_data) >= self.capacity:
                oldest_key = self.queue.pop(0)
                del self.cache_data[oldest_key]
                print("DISCARD: {}".format(oldest_key))
        else:
            self.queue.remove(key)

        self.cache_data[key] = item
        self.queue.append(key)
