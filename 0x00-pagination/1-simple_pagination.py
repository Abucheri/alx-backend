#!/usr/bin/env python3
"""
Simple pagination class for a dataset of popular baby names
"""

import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Returns a tuple of start and end index for pagination.
    This function provides a simple yet effective way to determine the range
    of indexes to retrieve for a given page in a paginated dataset.
    The start index is calculated as (page - 1) * page_size.
    Since page numbers are 1-indexed, we subtract 1 from the page number.
    The end index is calculated by adding the page_size to the start index.

    Args:
        page (int): Page number (1-indexed).
        page_size (int): Number of items per page.

    Returns:
        Tuple[int, int]: Start and end index for the requested page.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


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
        """
        Returns the requested page of the dataset.

        Args:
            page (int, optional): Page number (1-indexed). Defaults to 1.
            page_size (int, optional): Number of items per page.
                                           Defaults to 10.

        Returns:
            List[List]: Subset of dataset corresponding to the
                            requested page.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        dataset = self.dataset()
        start_index, end_index = index_range(page, page_size)
        if start_index < len(dataset):
            return dataset[start_index:end_index]
        return []
