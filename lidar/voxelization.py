import open3d as o3d


def voxelize_point_cloud(
    point_cloud: o3d.geometry.PointCloud,
    voxel_size: float,
) -> o3d.geometry.PointCloud:
    """
    Downsample a point cloud using a voxel grid.

    Parameters
    ----------
    point_cloud : o3d.geometry.PointCloud
        Input point cloud.
    voxel_size : float
        Size of each voxel in meters.

    Returns
    -------
    o3d.geometry.PointCloud
        Voxel-downsampled point cloud.

    Raises
    ------
    ValueError
        If voxel_size is not positive.
    """

    if voxel_size <= 0:
        raise ValueError("voxel_size must be greater than zero.")

    if point_cloud.is_empty():
        return point_cloud

    return point_cloud.voxel_down_sample(voxel_size=voxel_size)