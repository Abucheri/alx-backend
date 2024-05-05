#!/usr/bin/env python3
"""
Simple pagination class for a dataset of popular baby names
"""

import csv
import math
from typing import List, Tuple, Dict, Any


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
    This class represents a server handling pagination for a dataset
    of popular baby names. It has a class-level constant DATA_FILE set
    to "Popular_Baby_Names.csv", which is the filename of the dataset.
    The constructor method __init__ initializes the __dataset attribute
    to None.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        This method loads the dataset from the CSV file into memory and
        caches it. It returns the dataset as a list of lists, excluding
        the header row. The method is documented with a docstring describing
        its purpose and behavior.
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
        This method retrieves the requested page of the dataset.
        It takes two integer arguments: page (default value 1) and
        page_size (default value 10). Assertions are used to ensure that
        both arguments are positive integers. It retrieves the dataset using
        the dataset method and calculates the start and end indexes for the
        requested page using the index_range function. If the start index is
        within the range of the dataset, it returns the subset of the dataset
        corresponding to the requested page. Otherwise, it returns an empty
        list.The method is documented with a detailed docstring explaining its
        purpose, parameters, and return value.

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

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Returns a dictionary containing hypermedia pagination details.

        Args:
            page (int, optional): Page number (1-indexed). Defaults to 1.
            page_size (int, optional): Number of items per page
                                       Defaults to 10.

        Returns:
            Dict[str, Union[int, List[List], None]]: Dictionary containing
                                                     pagination details.
        """
        page_data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.__dataset) / page_size)

        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            "page_size": len(page_data),
            "page": page,
            "data": page_data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }
