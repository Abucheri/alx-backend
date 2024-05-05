#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
Overall, this script provides a robust solution for hypermedia pagination,
even in scenarios where items may have been deleted between queries.
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    __init__: Initializes two private attributes,
    __dataset and __indexed_dataset, both initially set to None.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        Method to retrieve and cache the dataset from a CSV file.
        If the dataset is not cached, it reads the CSV file and stores
        the dataset excluding the header row in __dataset. It then returns
        this dataset.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        Method to index the dataset by sorting position, starting at 0.
        If __indexed_dataset is not cached, it calls the dataset method to
        retrieve the dataset and creates an indexed version of it by mapping
        each row to its index in the dataset. It then returns this indexed
        dataset.
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
        Returns a dictionary containing hypermedia pagination details based on
        index.
        calculates the next_index based on the current index and page_size.
        It checks if the next_index is not None and if it's greater than or
        equal to the length of the indexed dataset. If so, it sets next_index
        to None. It then constructs the data list by iterating over the range
        from index to next_index and including only those indexes present in
        the indexed dataset. Finally, it returns a dictionary with all the
        pagination details.
        The script includes an assertion to ensure that the index is either
        None or an integer within the valid range of the indexed dataset.

        Args:
            index (int, optional): Current start index of the return page.
                                   Defaults to None.
            page_size (int, optional): Current page size. Defaults to 10.

        Returns:
            Dict: Dictionary containing pagination details.
                  index: Current start index of the return page.
                  data: The actual page of the dataset.
                  page_size: Current page size.
                  next_index: The next index to query with, or None if no
                              next page.
        """
        assert index is None or (isinstance(index, int)
                                 and 0 <= index < len(self.__indexed_dataset))

        next_index = index + page_size if index is not None else None

        if (next_index is not None
           and next_index >= len(self.__indexed_dataset)):
            next_index = None

        data = [self.__indexed_dataset[i] for i in range(index, next_index)
                if i in self.__indexed_dataset]

        return {
            "index": index,
            "data": data,
            "page_size": page_size,
            "next_index": next_index
        }
