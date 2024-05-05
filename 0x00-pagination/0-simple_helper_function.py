#!/usr/bin/env python3
"""
Simple helper function for pagination logic
"""

from typing import Tuple


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
