import numpy as np


def validate_point_cloud(points: np.ndarray) -> np.ndarray:
    """
    Validate and standardize a LiDAR point cloud.

    Standard output format:

    [x, y, z, intensity]
    """

    if points is None:
        raise ValueError("Point cloud is None.")

    if not isinstance(points, np.ndarray):
        raise TypeError(
            "Point cloud must be a NumPy array."
        )

    if points.size == 0:
        raise ValueError(
            "Point cloud is empty."
        )

    # Convert one-dimensional arrays if possible
    if points.ndim != 2:
        raise ValueError(
            f"Point cloud must be 2D. "
            f"Received shape: {points.shape}"
        )

    # At least XYZ is required
    if points.shape[1] < 3:
        raise ValueError(
            "Point cloud must contain at least X, Y and Z."
        )

    # Keep XYZ
    xyz = points[:, :3]

    # If intensity exists
    if points.shape[1] >= 4:
        intensity = points[:, 3:4]

    # Otherwise add intensity
    else:
        intensity = np.ones(
            (points.shape[0], 1),
            dtype=np.float32
        )

    # Standard format
    points = np.hstack((xyz, intensity))

    # Convert datatype
    points = points.astype(np.float32)

    # Remove NaN and infinity values
    valid_mask = np.isfinite(points).all(axis=1)

    points = points[valid_mask]

    if points.shape[0] == 0:
        raise ValueError(
            "No valid points remain after removing invalid values."
        )

    return points