import open3d as o3d
from pathlib import Path


def load_point_cloud(file_path: str) -> o3d.geometry.PointCloud:
    """
    Load a LiDAR point cloud from a file.

    Parameters
    ----------
    file_path : str
        Path to the point cloud file.

        
    Returns
    -------
    o3d.geometry.PointCloud
        Loaded point cloud.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Point cloud file not found: {file_path}")

    point_cloud = o3d.io.read_point_cloud(str(path))

    if point_cloud.is_empty():
        raise ValueError(f"Point cloud is empty: {file_path}")

    return point_cloud
