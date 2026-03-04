"""
Sorting, searching implementations
"""
import pandas as pd


def my_sort(arr, key):
    """My merge sort implementation with key support."""

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

def python_sort(arr, key):
    """Python built-in sort with key support"""
    return sorted(arr, key=key)

def my_search(arr, target, key):
    """My search implementation. E.g. binary search with key support"""
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

def pandas_search(arr, target, key):
    """Pandas search using .loc[] with key support."""

    df = pd.DataFrame(arr)
    mask = df.apply(lambda x: key(x) == key(target), axis=1)
    idx = df.loc[mask].index
    return idx[0] if len(idx) > 0 else -1