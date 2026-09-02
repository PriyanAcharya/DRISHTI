import numpy as np
import open3d as o3d


def remove_invalid_points(
    point_cloud: o3d.geometry.PointCloud,
) -> o3d.geometry.PointCloud:
    """
    Remove points containing NaN or infinite coordinates.

    Parameters
    ----------
    point_cloud : o3d.geometry.PointCloud
        Input point cloud.

    Returns
    -------
    o3d.geometry.PointCloud
        Point cloud containing only finite points.
    """

    points = np.asarray(point_cloud.points)

    if len(points) == 0:
        return point_cloud

    valid_mask = np.isfinite(points).all(axis=1)

    cleaned_cloud = point_cloud.select_by_index(
        np.where(valid_mask)[0]
    )

    return cleaned_cloud


def remove_statistical_outliers(
    point_cloud: o3d.geometry.PointCloud,
    nb_neighbors: int = 20,
    std_ratio: float = 2.0,
) -> o3d.geometry.PointCloud:
    """
    Remove statistical outliers from a point cloud.

    Parameters
    ----------
    point_cloud : o3d.geometry.PointCloud
        Input point cloud.
    nb_neighbors : int
        Number of neighboring points used for analysis.
    std_ratio : float
        Standard deviation multiplier used to identify outliers.

    Returns
    -------
    o3d.geometry.PointCloud
        Filtered point cloud.
    """

    if len(point_cloud.points) == 0:
        return point_cloud

    if len(point_cloud.points) <= nb_neighbors:
        return point_cloud

    filtered_cloud, _ = point_cloud.remove_statistical_outlier(
        nb_neighbors=nb_neighbors,
        std_ratio=std_ratio,
    )

    return filtered_cloud


def preprocess_point_cloud(
    point_cloud: o3d.geometry.PointCloud,
    nb_neighbors: int = 20,
    std_ratio: float = 2.0,
) -> o3d.geometry.PointCloud:
    """
    Run the complete LiDAR preprocessing pipeline.

    Steps:
    1. Remove invalid points.
    2. Remove statistical outliers.

    Parameters
    ----------
    point_cloud : o3d.geometry.PointCloud
        Raw loaded point cloud.
    nb_neighbors : int
        Number of neighbors for statistical filtering.
    std_ratio : float
        Standard deviation threshold for statistical filtering.

    Returns
    -------
    o3d.geometry.PointCloud
        Cleaned point cloud.
    """

    cleaned_cloud = remove_invalid_points(point_cloud)

    cleaned_cloud = remove_statistical_outliers(
        cleaned_cloud,
        nb_neighbors=nb_neighbors,
        std_ratio=std_ratio,
    )

    return cleaned_cloud