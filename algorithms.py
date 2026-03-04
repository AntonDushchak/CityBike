"""Custom sorting and searching algorithm implementations."""

from typing import Any, Callable, List, TypeVar

import pandas as pd

T = TypeVar("T")


def my_sort(arr: List[T], key: Callable[[T], Any]) -> List[T]:
    """Merge sort implementation with key support.

    Time complexity: O(n log n)
    Space complexity: O(n)

    Args:
        arr: List of items to sort.
        key: Function to extract comparison key from each item.

    Returns:
        New sorted list.
    """

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = my_sort(arr[:mid], key)
    right = my_sort(arr[mid:], key)

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def python_sort(arr: List[T], key: Callable[[T], Any]) -> List[T]:
    """Python built-in sort with key support.

    Time complexity: O(n log n) - Timsort

    Args:
        arr: List of items to sort.
        key: Function to extract comparison key.

    Returns:
        New sorted list.
    """
    return sorted(arr, key=key)


def my_search(arr: List[T], target: T, key: Callable[[T], Any]) -> int:
    """Binary search implementation with key support.

    Time complexity: O(log n)
    Requires arr to be sorted by key.

    Args:
        arr: Sorted list of items.
        target: Item to search for.
        key: Function to extract comparison key.

    Returns:
        Index of target if found, -1 otherwise.
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if key(arr[mid]) == key(target):
            return mid

        if key(arr[mid]) < key(target):
            left = mid + 1
        else:
            right = mid - 1

    return -1


def pandas_search(arr: List[T], target: T, key: Callable[[T], Any]) -> int:
    """Search using pandas DataFrame filtering.

    Time complexity: O(n)

    Args:
        arr: List of items (converted to DataFrame).
        target: Item to search for.
        key: Function to extract comparison key.

    Returns:
        Index of first match if found, -1 otherwise.
    """

    df = pd.DataFrame(arr)
    mask = df.apply(lambda x: key(x) == key(target), axis=1)
    idx = df.loc[mask].index
    return idx[0] if len(idx) > 0 else -1