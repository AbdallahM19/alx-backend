#!/usr/bin/env python3
"""0. Simple helper function"""

def index_range(page, page_size):
    """
    a function named index_range that
    takes two integer arguments page and page_size
    """
    end_page = page * page_size
    start_page = end_page - page_size
    return (start_page, end_page)
