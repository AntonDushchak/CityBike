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
