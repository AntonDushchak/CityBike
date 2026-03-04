"""Custom sorting and searching algorithm implementations."""

from timeit import timeit
from typing import Any, Callable, Dict, List, Optional, TypeVar

import pandas as pd

T = TypeVar("T")

BENCHMARK_SAMPLE_SIZE = 2000
BENCHMARK_SORT_RUNS = 5
BENCHMARK_SEARCH_RUNS = 250
TRIP_PREVIEW_COUNT = 5
STATION_SAMPLE_INDEX = 0

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

def run_algorithm_demo(
    trips_df: Optional[pd.DataFrame],
    stations_df: Optional[pd.DataFrame],
) -> Dict[str, object]:
    """Run my_sort/my_search on real trip and station data.

    Args:
        trips_df: Cleaned trips DataFrame.
        stations_df: Cleaned stations DataFrame.

    Returns:
        Dictionary with sorted IDs, search results, and messages.
    """
    result: Dict[str, object] = {
        "trip_sort_ids": None,
        "trip_search": None,
        "station_search": None,
        "messages": [],
    }

    if trips_df is not None and not trips_df.empty and "trip_id" in trips_df:
        trip_columns = [
            col
            for col in ["trip_id", "start_station_id", "duration_minutes", "distance_km", "user_type"]
            if col in trips_df
        ]
        trip_records = trips_df[trip_columns].to_dict("records")
        if trip_records:
            sort_key_trip = lambda row: row["trip_id"]
            sorted_trips = my_sort(trip_records, key=sort_key_trip)
            result["trip_sort_ids"] = [row["trip_id"] for row in sorted_trips[:TRIP_PREVIEW_COUNT]]
            target_trip = sorted_trips[len(sorted_trips) // 2]
            trip_index = my_search(sorted_trips, target_trip, key=sort_key_trip)
            result["trip_search"] = {
                "trip_id": target_trip["trip_id"],
                "index": trip_index,
            }
        else:
            result["messages"].append("Trip dataset empty after conversion; custom algorithms skipped.")
    else:
        result["messages"].append("Trip data unavailable for custom algorithm demo.")

    if stations_df is not None and not stations_df.empty and "station_id" in stations_df:
        station_columns = [col for col in ["station_id", "station_name", "capacity"] if col in stations_df]
        station_records = stations_df[station_columns].to_dict("records")
        if station_records:
            sort_key_station = lambda row: row["station_id"]
            sorted_stations = my_sort(station_records, key=sort_key_station)
            target_station = sorted_stations[STATION_SAMPLE_INDEX]
            station_index = my_search(sorted_stations, target_station, key=sort_key_station)
            result["station_search"] = {
                "station_id": target_station["station_id"],
                "station_name": target_station.get("station_name"),
                "index": station_index,
            }
        else:
            result["messages"].append("Station dataset empty after conversion; station search skipped.")
    else:
        result["messages"].append("Station data unavailable for custom algorithm demo.")

    return result

def run_benchmark(
    trips_df: Optional[pd.DataFrame],
    sample_size: int = BENCHMARK_SAMPLE_SIZE,
) -> Dict[str, Optional[object]]:
    """Compare custom vs native algorithms using timeit.

    Args:
        trips_df: Cleaned trips DataFrame for benchmarking.
        sample_size: Number of records to use in benchmark.

    Returns:
        Dictionary with benchmark results and optional figure path.
    """
    if trips_df is None or trips_df.empty or "trip_id" not in trips_df:
        return {"results": None, "figure_path": None, "message": "Missing trip data for benchmarks."}

    subset_columns = [
        col for col in ["trip_id", "duration_minutes", "distance_km", "user_type"] if col in trips_df
    ]
    trip_sample = trips_df[subset_columns].head(sample_size).to_dict("records")
    if not trip_sample:
        return {"results": None, "figure_path": None, "message": "Insufficient trip sample for benchmarks."}

    sort_key = lambda row: row["trip_id"]
    my_sort_time = timeit(lambda: my_sort(trip_sample, sort_key), number=BENCHMARK_SORT_RUNS)
    python_sort_time = timeit(lambda: python_sort(trip_sample, sort_key), number=BENCHMARK_SORT_RUNS)

    sorted_sample = python_sort(trip_sample, sort_key)
    if not sorted_sample:
        return {"results": None, "figure_path": None, "message": "Sorted sample empty; benchmarks aborted."}

    target = sorted_sample[len(sorted_sample) // 2]
    my_search_time = timeit(lambda: my_search(sorted_sample, target, sort_key), number=BENCHMARK_SEARCH_RUNS)
    pandas_search_time = timeit(lambda: pandas_search(sorted_sample, target, sort_key), number=BENCHMARK_SEARCH_RUNS)

    benchmark_results = {
        "my_sort": my_sort_time / BENCHMARK_SORT_RUNS,
        "python_sort": python_sort_time / BENCHMARK_SORT_RUNS,
        "my_search": my_search_time / BENCHMARK_SEARCH_RUNS,
        "pandas_search": pandas_search_time / BENCHMARK_SEARCH_RUNS,
    }

    return {"results": benchmark_results, "figure_path": None, "message": None}