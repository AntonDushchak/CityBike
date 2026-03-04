## Optional Analysis: Sorting and Searching Algorithms

### Time Complexity (Big-O) for Each Implementation

#### Sorting
- **my_sort (Quick Sort, custom)**: Average O(n log n), Worst O(n^2)
- **python_sort (built-in sorted)**: O(n log n) (Timsort)

#### Searching
- **my_search (Binary Search, custom)**: O(log n) (requires sorted input)
- **pandas_search / pandas_loc_search / pandas_query_search**: O(n) for general DataFrame search (since each row is checked)

### Performance Comparison

- **Built-in sorted (Timsort)** is highly optimized in C and handles real-world data patterns efficiently, making it faster than most pure Python implementations.
- **Custom quick sort (my_sort)** is slower due to Python-level recursion and lack of low-level optimizations.
- **Binary search (my_search)** is fast (O(log n)), but only works on sorted data.
- **Pandas search** is convenient for tabular data, but not faster than native Python for small lists; for large DataFrames, vectorized operations are preferred.

### Why Built-in Functions Are Typically Faster

Built-in functions like `sorted`, `list.index`, and pandas vectorized methods are implemented in highly optimized C code, which:
- Reduces Python interpreter overhead
- Uses efficient memory access patterns
- Employs advanced algorithms (e.g., Timsort for sorting)
- Leverages CPU-level optimizations

As a result, built-in functions are usually much faster than equivalent algorithms written in pure Python, especially on large datasets.