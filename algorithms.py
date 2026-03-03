"""
Sorting, searching implementations
"""
import pandas as pd

def my_sort(arr, key):
    """My sort implementation. E.g. quick sort with key support"""
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if key(x) < key(pivot)]
    right = [x for x in arr[1:] if key(x) >= key(pivot)]
    return my_sort(left, key) + [pivot] + my_sort(right, key)


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
    """Pandas search implementation. E.g. boolean indexing"""
    
    df = pd.DataFrame(arr)
    result = df[df.apply(lambda x: key(x) == key(target), axis=1)]
    return result.index[0] if not result.empty else -1