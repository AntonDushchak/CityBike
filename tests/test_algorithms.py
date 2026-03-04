"""Tests for sorting and searching algorithms in algorithms.py."""

import pytest

from algorithms import my_search, my_sort, pandas_search, python_sort

class TestMergeSort:
    """Tests for custom merge sort implementation."""

    def test_sort_empty_list(self) -> None:
        """Test sorting an empty list returns empty list."""
        result = my_sort([], key=lambda x: x)
        assert result == []

    def test_sort_single_element(self) -> None:
        """Test sorting a single-element list returns same list."""
        result = my_sort([42], key=lambda x: x)
        assert result == [42]

    def test_sort_integers_ascending(self) -> None:
        """Test sorting integers in ascending order."""
        data = [5, 2, 8, 1, 9, 3]
        result = my_sort(data, key=lambda x: x)
        assert result == [1, 2, 3, 5, 8, 9]

    def test_sort_already_sorted(self) -> None:
        """Test sorting an already sorted list."""
        data = [1, 2, 3, 4, 5]
        result = my_sort(data, key=lambda x: x)
        assert result == [1, 2, 3, 4, 5]

    def test_sort_reverse_order(self) -> None:
        """Test sorting a reverse-ordered list."""
        data = [5, 4, 3, 2, 1]
        result = my_sort(data, key=lambda x: x)
        assert result == [1, 2, 3, 4, 5]

    def test_sort_with_duplicates(self) -> None:
        """Test sorting a list with duplicate values."""
        data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        result = my_sort(data, key=lambda x: x)
        assert result == sorted(data)

    def test_sort_strings_alphabetically(self) -> None:
        """Test sorting strings alphabetically."""
        data = ["banana", "apple", "cherry", "date"]
        result = my_sort(data, key=lambda x: x)
        assert result == ["apple", "banana", "cherry", "date"]

    def test_sort_dicts_by_key(self) -> None:
        """Test sorting dictionaries by a specific key."""
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35},
        ]
        result = my_sort(data, key=lambda x: x["age"])
        assert result[0]["name"] == "Bob"
        assert result[1]["name"] == "Alice"
        assert result[2]["name"] == "Charlie"

    def test_sort_preserves_original(self) -> None:
        """Test that sorting does not modify the original list."""
        data = [3, 1, 4, 1, 5]
        original = data.copy()
        my_sort(data, key=lambda x: x)
        assert data == original

    def test_sort_matches_python_sort(self) -> None:
        """Test that custom sort produces same result as Python's sorted."""
        data = [64, 34, 25, 12, 22, 11, 90]
        custom_result = my_sort(data, key=lambda x: x)
        python_result = python_sort(data, key=lambda x: x)
        assert custom_result == python_result

    def test_sort_trip_records_by_id(self) -> None:
        """Test sorting trip-like records by trip_id."""
        trips = [
            {"trip_id": "TR003", "distance": 5.0},
            {"trip_id": "TR001", "distance": 3.5},
            {"trip_id": "TR002", "distance": 7.2},
        ]
        result = my_sort(trips, key=lambda x: x["trip_id"])
        assert result[0]["trip_id"] == "TR001"
        assert result[1]["trip_id"] == "TR002"
        assert result[2]["trip_id"] == "TR003"

    def test_sort_by_numeric_field(self) -> None:
        """Test sorting records by a numeric field (like duration)."""
        trips = [
            {"trip_id": "TR001", "duration_minutes": 45},
            {"trip_id": "TR002", "duration_minutes": 15},
            {"trip_id": "TR003", "duration_minutes": 30},
        ]
        result = my_sort(trips, key=lambda x: x["duration_minutes"])
        assert result[0]["duration_minutes"] == 15
        assert result[1]["duration_minutes"] == 30
        assert result[2]["duration_minutes"] == 45

class TestBinarySearch:
    """Tests for custom binary search implementation."""

    def test_search_finds_element_at_start(self) -> None:
        """Test finding an element at the start of the list."""
        data = [1, 2, 3, 4, 5]
        result = my_search(data, 1, key=lambda x: x)
        assert result == 0

    def test_search_finds_element_at_end(self) -> None:
        """Test finding an element at the end of the list."""
        data = [1, 2, 3, 4, 5]
        result = my_search(data, 5, key=lambda x: x)
        assert result == 4

    def test_search_finds_element_in_middle(self) -> None:
        """Test finding an element in the middle of the list."""
        data = [1, 2, 3, 4, 5]
        result = my_search(data, 3, key=lambda x: x)
        assert result == 2

    def test_search_element_not_found(self) -> None:
        """Test searching for non-existent element returns -1."""
        data = [1, 2, 3, 4, 5]
        result = my_search(data, 10, key=lambda x: x)
        assert result == -1

    def test_search_empty_list(self) -> None:
        """Test searching in empty list returns -1."""
        result = my_search([], 5, key=lambda x: x)
        assert result == -1

    def test_search_single_element_found(self) -> None:
        """Test searching in single-element list when element exists."""
        result = my_search([42], 42, key=lambda x: x)
        assert result == 0

    def test_search_single_element_not_found(self) -> None:
        """Test searching in single-element list when element doesn't exist."""
        result = my_search([42], 10, key=lambda x: x)
        assert result == -1

    def test_search_dicts_by_key(self) -> None:
        """Test searching dictionaries by a specific key."""
        data = [
            {"id": "A", "value": 10},
            {"id": "B", "value": 20},
            {"id": "C", "value": 30},
        ]
        target = {"id": "B", "value": 20}
        result = my_search(data, target, key=lambda x: x["id"])
        assert result == 1

    def test_search_trip_by_id(self) -> None:
        """Test searching for a trip by trip_id."""
        trips = [
            {"trip_id": "TR001", "distance": 3.5},
            {"trip_id": "TR002", "distance": 7.2},
            {"trip_id": "TR003", "distance": 5.0},
        ]
        target = {"trip_id": "TR002", "distance": 7.2}
        result = my_search(trips, target, key=lambda x: x["trip_id"])
        assert result == 1

class TestPandasSearch:
    """Tests for pandas-based search implementation."""

    def test_pandas_search_finds_element(self) -> None:
        """Test that pandas search finds existing element."""
        data = [
            {"id": "A", "value": 10},
            {"id": "B", "value": 20},
            {"id": "C", "value": 30},
        ]
        target = {"id": "B", "value": 20}
        result = pandas_search(data, target, key=lambda x: x["id"])
        assert result == 1

    def test_pandas_search_element_not_found(self) -> None:
        """Test that pandas search returns -1 for non-existent element."""
        data = [
            {"id": "A", "value": 10},
            {"id": "B", "value": 20},
        ]
        target = {"id": "X", "value": 99}
        result = pandas_search(data, target, key=lambda x: x["id"])
        assert result == -1

class TestPythonSort:
    """Tests for Python built-in sort wrapper."""

    def test_python_sort_integers(self) -> None:
        """Test Python sort with integers."""
        data = [5, 2, 8, 1, 9]
        result = python_sort(data, key=lambda x: x)
        assert result == [1, 2, 5, 8, 9]

    def test_python_sort_preserves_original(self) -> None:
        """Test that Python sort does not modify original list."""
        data = [3, 1, 4, 1, 5]
        original = data.copy()
        python_sort(data, key=lambda x: x)
        assert data == original

    def test_python_sort_with_custom_key(self) -> None:
        """Test Python sort with custom key function."""
        data = [{"x": 3}, {"x": 1}, {"x": 2}]
        result = python_sort(data, key=lambda d: d["x"])
        assert result[0]["x"] == 1
        assert result[1]["x"] == 2
        assert result[2]["x"] == 3