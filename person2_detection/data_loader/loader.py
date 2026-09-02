from pathlib import Path
import numpy as np


def load_bin(file_path: str) -> np.ndarray:
    """
    Load a KITTI-style LiDAR .bin file.

    Expected format:
    [x, y, z, intensity]
    """

    points = np.fromfile(file_path, dtype=np.float32)

    if points.size % 4 != 0:
        raise ValueError(
            "Invalid .bin file. Number of values is not divisible by 4."
        )

    points = points.reshape(-1, 4)

    return points


def load_npy(file_path: str) -> np.ndarray:
    """
    Load a NumPy point cloud file.
    """

    points = np.load(file_path)

    return points


def load_pcd(file_path: str) -> np.ndarray:
    """
    Load a PCD point cloud file.

    Requires Open3D.
    """

    try:
        import open3d as o3d
    except ImportError:
        raise ImportError(
            "Open3D is required for PCD files. "
            "Install it using: pip install open3d"
        )

    point_cloud = o3d.io.read_point_cloud(file_path)

    xyz = np.asarray(point_cloud.points)

    if xyz.size == 0:
        raise ValueError("PCD file contains no points.")

    # Open3D may not provide intensity.
    # Add intensity = 1.0.
    intensity = np.ones((xyz.shape[0], 1), dtype=np.float32)

    points = np.hstack((xyz, intensity))

    return points.astype(np.float32)


def load_point_cloud(file_path: str) -> np.ndarray:
    """
    Automatically load a supported LiDAR point cloud.

    Supported formats:
    - .bin
    - .npy
    - .pcd
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Point cloud file not found: {file_path}"
        )

    suffix = path.suffix.lower()

    if suffix == ".bin":
        points = load_bin(str(path))

    elif suffix == ".npy":
        points = load_npy(str(path))

    elif suffix == ".pcd":
        points = load_pcd(str(path))

    else:
        raise ValueError(
            f"Unsupported file format: {suffix}. "
            "Supported formats are .bin, .npy and .pcd"
        )

    return points