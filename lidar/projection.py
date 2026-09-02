import numpy as np
import pandas as pd
import open3d as o3d


def project_to_2_5d(
    point_cloud: o3d.geometry.PointCloud,
    grid_size: float = 0.5,
) -> pd.DataFrame:
    """
    Project a 3D point cloud onto an XY-based 2.5D grid.

    Each grid cell stores:
    - X/Y grid location
    - maximum height
    - number of points
    - elevation variation

    Parameters
    ----------
    point_cloud : o3d.geometry.PointCloud
        Input 3D point cloud.
    grid_size : float
        Width and height of each XY grid cell in meters.

    Returns
    -------
    pandas.DataFrame
        2.5D grid representation.

    Raises
    ------
    ValueError
        If grid_size is not positive.
    """

    if grid_size <= 0:
        raise ValueError("grid_size must be greater than zero.")

    points = np.asarray(point_cloud.points)

    if len(points) == 0:
        return pd.DataFrame(
            columns=[
                "grid_x",
                "grid_y",
                "height",
                "point_density",
                "elevation_variation",
            ]
        )

    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]

    grid_x = np.floor(x / grid_size).astype(int)
    grid_y = np.floor(y / grid_size).astype(int)

    data = pd.DataFrame({
        "grid_x": grid_x,
        "grid_y": grid_y,
        "z": z,
    })

    grouped = data.groupby(["grid_x", "grid_y"])

    projection = grouped["z"].agg(
        height="max",
        point_density="count",
        elevation_variation=lambda values: values.max() - values.min(),
    ).reset_index()

    return projection