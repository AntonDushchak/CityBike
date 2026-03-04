"""NumPy-based numerical computations for distance, statistics, and outliers."""

from typing import Any, Dict, List, Union

import numpy as np
from numpy.typing import ArrayLike, NDArray

def calculate_statistics(data: ArrayLike) -> Dict[str, float]:
    """Calculate statistical metrics for a dataset.

    Args:
        data: Input array-like data.

    Returns:
        Dictionary with mean, median, variance, std, min, max, count.
    """
    
    data = np.array(data)

    return {
        "mean": data.mean(),
        "median": np.median(data),
        "variance": data.var(),
        "std": data.std(),
        "min": data.min(),
        "max": data.max(),
        "count": data.size
    }

def compute_distance_matrix(
    positions1: ArrayLike, positions2: ArrayLike
) -> NDArray[np.floating[Any]]:
    """Compute distance matrix between two sets of positions using Euclidean distance.

    Uses simplified flat-earth model (not Haversine).

    Args:
        positions1: Array of (lat, lon) coordinates, shape (n, 2).
        positions2: Array of (lat, lon) coordinates, shape (m, 2).

    Returns:
        Distance matrix of shape (n, m).
    """

    pos1 = np.asarray(positions1)
    pos2 = np.asarray(positions2)

    dlat = pos1[:, np.newaxis, 0] - pos2[np.newaxis, :, 0]
    dlon = pos1[:, np.newaxis, 1] - pos2[np.newaxis, :, 1]
    dist = np.sqrt(dlat ** 2 + dlon ** 2)
    return dist

def normalize_data(
    data: ArrayLike, axis: int = -1, order: int = 2
) -> NDArray[np.floating[Any]]:
    """Normalize data along specified axis using L-norm.

    Args:
        data: Input array.
        axis: Axis along which to normalize.
        order: Order of the norm (default L2).

    Returns:
        Normalized array.
    """
    l2 = np.atleast_1d(np.linalg.norm(data, order, axis))
    l2[l2 == 0] = 1
    return data / np.expand_dims(l2, axis)

def batch_calculate_fares(
    distances_km: ArrayLike,
    base_rate: float = 1.0,
    per_km_rate: float = 0.5,
    min_fare: float = 2.0,
) -> NDArray[np.floating[Any]]:
    """Calculate fares for multiple trips using vectorized operations.

    Args:
        distances_km: Array of trip distances.
        base_rate: Base fare amount.
        per_km_rate: Rate per kilometer.
        min_fare: Minimum fare amount.

    Returns:
        Array of fare amounts.
    """

    distances = np.asarray(distances_km)
    fares = base_rate + (distances * per_km_rate)
    return np.maximum(fares, min_fare)

def batch_calculate_fares_with_strategy(
    distances_km: ArrayLike, strategy_rates: ArrayLike, min_fare: float = 2.0
) -> NDArray[np.floating[Any]]:
    """Calculate fares using different pricing strategies per trip.

    Args:
        distances_km: Array of trip distances.
        strategy_rates: Array of rates corresponding to each trip.
        min_fare: Minimum fare amount.

    Returns:
        Array of fare amounts.
    """

    distances = np.asarray(distances_km)
    rates = np.asarray(strategy_rates)
    fares = distances * rates
    return np.maximum(fares, min_fare)

def detect_outliers_zscore(
    data: ArrayLike, threshold: float = 3.0
) -> Dict[str, Union[NDArray[Any], float]]:
    """Detect outliers using Z-score method.

    Args:
        data: Input array.
        threshold: Z-score threshold for outlier detection.

    Returns:
        Dictionary with outlier_mask, outlier_indices, outlier_values,
        z_scores, mean, and std.
    """

    data = np.asarray(data)
    mean = np.mean(data)
    std = np.std(data)
    
    if std == 0:
        return {
            "outlier_mask": np.zeros(len(data), dtype=bool),
            "outlier_indices": np.array([], dtype=int),
            "outlier_values": np.array([]),
            "z_scores": np.zeros(len(data)),
            "mean": mean,
            "std": std
        }
    
    z_scores = np.abs((data - mean) / std)
    outlier_mask = z_scores > threshold
    
    return {
        "outlier_mask": outlier_mask,
        "outlier_indices": np.where(outlier_mask)[0],
        "outlier_values": data[outlier_mask],
        "z_scores": z_scores,
        "mean": mean,
        "std": std
    }

def remove_outliers_zscore(
    data: ArrayLike, threshold: float = 3.0
) -> NDArray[np.floating[Any]]:
    """Remove outliers from data using Z-score method.

    Args:
        data: Input array.
        threshold: Z-score threshold.

    Returns:
        Array with outliers removed.
    """
    
    result = detect_outliers_zscore(data, threshold)
    return np.asarray(data)[~result["outlier_mask"]]