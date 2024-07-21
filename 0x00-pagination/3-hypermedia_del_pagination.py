#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Implement a get_hyper_index method with two
        integer arguments: index with a None default value
        and page_size with default value of 10
        """
        indexed_dataset = self.indexed_dataset()

        assert isinstance(index, int) and type(index) == int
        assert isinstance(page_size, int) and type(page_size) == int

        next_index = index
        data = []

        dataset_len = len(indexed_dataset)

        while True:
            if len(data) < page_size and next_index < dataset_len:
                if next_index in indexed_dataset:
                    data.append(indexed_dataset[next_index])
                next_index += 1
            else:
                break

        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data,
        }
