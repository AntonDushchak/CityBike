"""
NumPy-based computations
"""

import numpy as np

def calculate_statistics(data):
    """Calculate statistical metrics"""
    
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

def compute_distance_matrix(positions1, positions2):
    """
    Compute distance matrix between two sets of positions (lat, lon) using Euclidean distance.
    """

    pos1 = np.asarray(positions1)
    pos2 = np.asarray(positions2)

    dlat = pos1[:, np.newaxis, 0] - pos2[np.newaxis, :, 0]
    dlon = pos1[:, np.newaxis, 1] - pos2[np.newaxis, :, 1]
    dist = np.sqrt(dlat ** 2 + dlon ** 2)
    return dist

def normalize_data(data, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(data, order, axis))
    l2[l2==0] = 1
    return data / np.expand_dims(l2, axis)

def batch_calculate_fares(distances_km, base_rate=1.0, per_km_rate=0.5, min_fare=2.0):
    """
    Calculate fares for multiple trips in batch using vectorized operations.
    """

    distances = np.asarray(distances_km)
    fares = base_rate + (distances * per_km_rate)
    return np.maximum(fares, min_fare)

def batch_calculate_fares_with_strategy(distances_km, strategy_rates, min_fare=2.0):
    """
    Calculate fares for multiple trips with different pricing strategies.
    """

    distances = np.asarray(distances_km)
    rates = np.asarray(strategy_rates)
    fares = distances * rates
    return np.maximum(fares, min_fare)

def detect_outliers_zscore(data, threshold=3.0):
    """
    Detect outliers using Z-score method.
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

def remove_outliers_zscore(data, threshold=3.0):
    """
    Remove outliers from data using Z-score method.
    """
    
    result = detect_outliers_zscore(data, threshold)
    return np.asarray(data)[~result["outlier_mask"]]
