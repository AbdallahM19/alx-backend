#!/usr/bin/env python3
"""1. Simple pagination"""

import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    a function named index_range that
    takes two integer arguments page and page_size
    """
    end_page = page * page_size
    start_page = end_page - page_size
    return (start_page, end_page)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """get data for page"""
        assert type(page) == int and type(page_size) == int
        assert page > 0 and page_size > 0
        start_page, end_page = index_range(page, page_size)
        data_page = self.dataset()
        return [] if start_page > len(data_page)\
            else data_page[start_page:end_page]
