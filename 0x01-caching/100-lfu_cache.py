#!/usr/bin/python3
"""cache system"""

from collections import defaultdict

BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """a class LFUCache that inherits from BaseCaching"""
    def __init__(self):
        """init method"""
        super().__init__()
        self.capacity = BaseCaching.MAX_ITEMS
        self.frequency = defaultdict(int)
        self.usage_order = {}

    def put(self, key, item):
        """add an item to the cache"""
        if key is None or item is None:
            return

        if key not in self.cache_data:
            if len(self.cache_data) >= self.capacity:
                lfu_keys = [
                    k for k, v in self.frequency.items() if v == min(
                        self.frequency.values()
                    )
                ]
                if len(lfu_keys) > 1:
                    lru_key = min(
                        lfu_keys, key=lambda k: self.usage_order[k]
                    )
                else:
                    lru_key = lfu_keys[0]

                del self.cache_data[lru_key]
                del self.frequency[lru_key]
                del self.usage_order[lru_key]
                print("DISCARD: {}".format(lru_key))

        self.cache_data[key] = item
        self.frequency[key] += 1
        self.usage_order[key] = len(self.usage_order)

    def get(self, key):
        """get an item from the cache"""
        if key is None or key not in self.cache_data:
            return None

        self.frequency[key] += 1
        self.usage_order[key] = len(self.usage_order)
        return self.cache_data.get(key)
