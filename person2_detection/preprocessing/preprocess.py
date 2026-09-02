import numpy as np


def filter_by_range(
    points: np.ndarray,
    x_range=(-50.0, 50.0),
    y_range=(-50.0, 50.0),
    z_range=(-5.0, 5.0)
) -> np.ndarray:
    """
    Remove points outside the configured LiDAR range.
    """

    mask = (
        (points[:, 0] >= x_range[0]) &
        (points[:, 0] <= x_range[1]) &

        (points[:, 1] >= y_range[0]) &
        (points[:, 1] <= y_range[1]) &

        (points[:, 2] >= z_range[0]) &
        (points[:, 2] <= z_range[1])
    )

    return points[mask]


def remove_zero_points(
    points: np.ndarray
) -> np.ndarray:
    """
    Remove points located exactly at the origin.
    """

    mask = np.any(
        points[:, :3] != 0,
        axis=1
    )

    return points[mask]


def preprocess_point_cloud(
    points: np.ndarray
) -> np.ndarray:
    """
    Basic preprocessing pipeline.
    """

    # Remove origin points
    points = remove_zero_points(points)

    # Apply spatial filtering
    points = filter_by_range(points)

    if len(points) == 0:
        raise ValueError(
            "No points remain after preprocessing."
        )

    return points