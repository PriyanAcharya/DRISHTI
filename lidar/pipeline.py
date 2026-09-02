import open3d as o3d
import pandas as pd

from lidar.loader import load_point_cloud
from lidar.preprocessing import preprocess_point_cloud
from lidar.voxelization import voxelize_point_cloud
from lidar.projection import project_to_2_5d


def run_lidar_pipeline(
    file_path: str,
    voxel_size: float = 0.5,
    grid_size: float = 0.5,
    nb_neighbors: int = 20,
    std_ratio: float = 2.0,
) -> tuple[o3d.geometry.PointCloud, pd.DataFrame]:
    """
    Run the complete LiDAR processing pipeline.

    Processing steps:
    1. Load the raw point cloud.
    2. Remove invalid points and statistical outliers.
    3. Voxelize the cleaned point cloud.
    4. Project the voxelized cloud into a 2.5D grid.

    Parameters
    ----------
    file_path : str
        Path to the input LiDAR point-cloud file.
    voxel_size : float
        Voxel size in meters.
    grid_size : float
        2.5D XY grid size in meters.
    nb_neighbors : int
        Number of neighbors used for statistical filtering.
    std_ratio : float
        Standard deviation threshold for statistical filtering.

    Returns
    -------
    tuple
        - voxelized point cloud
        - 2.5D pandas DataFrame
    """

    point_cloud = load_point_cloud(file_path)

    cleaned_cloud = preprocess_point_cloud(
        point_cloud,
        nb_neighbors=nb_neighbors,
        std_ratio=std_ratio,
    )

    voxelized_cloud = voxelize_point_cloud(
        cleaned_cloud,
        voxel_size=voxel_size,
    )

    map_2_5d = project_to_2_5d(
        voxelized_cloud,
        grid_size=grid_size,
    )

    return voxelized_cloud, map_2_5d