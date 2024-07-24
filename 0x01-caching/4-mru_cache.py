#!/usr/bin/python3
"""cache system"""

from collections import OrderedDict

BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """a class MRUCache that inherits from BaseCaching"""
    def __init__(self):
        """init method"""
        super().__init__()
        self.capacity = BaseCaching.MAX_ITEMS
        self.order = OrderedDict()

    def put(self, key, item):
        """add an item to the cache"""
        if key is None or item is None:
            return

        self.cache_data[key] = item

        if len(self.cache_data) > self.capacity:
            dis_key, dis_item = self.order.popitem(last=True)
            del self.cache_data[dis_key]
            print("DISCARD: {}".format(dis_key))

        self.order[key] = item
        self.order.move_to_end(key)

    def get(self, key):
        """get an item from the cache"""
        if key is None or key not in self.cache_data:
            return None
        self.order.move_to_end(key)
        return self.cache_data.get(key)
