import numpy as np
import open3d as o3d

from lidar.pipeline import run_lidar_pipeline
from lidar.projection import project_to_2_5d
from lidar.voxelization import voxelize_point_cloud
from lidar.loader import load_point_cloud
from lidar.preprocessing import (
    remove_invalid_points,
    remove_statistical_outliers,
    preprocess_point_cloud,
)


def test_load_point_cloud(tmp_path):
    points = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ])

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    test_file = tmp_path / "test_cloud.ply"
    o3d.io.write_point_cloud(str(test_file), point_cloud)

    loaded_cloud = load_point_cloud(str(test_file))

    assert not loaded_cloud.is_empty()
    assert len(loaded_cloud.points) == 3


def test_remove_invalid_points():
    points = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 1.0, 1.0],
        [np.nan, 2.0, 2.0],
        [np.inf, 3.0, 3.0],
    ])

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    cleaned_cloud = remove_invalid_points(point_cloud)

    assert len(cleaned_cloud.points) == 2
    assert np.isfinite(np.asarray(cleaned_cloud.points)).all()


def test_remove_statistical_outliers():
    # Create a small cluster of nearby points plus one distant point.
    points = np.array([
        [0.00, 0.00, 0.00],
        [0.05, 0.00, 0.00],
        [0.00, 0.05, 0.00],
        [0.05, 0.05, 0.00],
        [0.02, 0.02, 0.02],
        [0.03, 0.01, 0.02],
        [10.0, 10.0, 10.0],
    ])

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    filtered_cloud = remove_statistical_outliers(
        point_cloud,
        nb_neighbors=3,
        std_ratio=1.0,
    )

    assert len(filtered_cloud.points) < len(point_cloud.points)


def test_preprocess_point_cloud():
    points = np.array([
        [0.00, 0.00, 0.00],
        [0.05, 0.00, 0.00],
        [0.00, 0.05, 0.00],
        [0.05, 0.05, 0.00],
        [0.02, 0.02, 0.02],
        [0.03, 0.01, 0.02],
        [10.0, 10.0, 10.0],
    ])

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    cleaned_cloud = preprocess_point_cloud(
        point_cloud,
        nb_neighbors=3,
        std_ratio=1.0,
    )

    assert not cleaned_cloud.is_empty()
    assert len(cleaned_cloud.points) < len(point_cloud.points)
def test_voxelize_point_cloud():
    # Create several points that fall into nearby voxels.
    points = np.array([
        [0.00, 0.00, 0.00],
        [0.05, 0.05, 0.05],
        [0.10, 0.10, 0.10],
        [1.00, 1.00, 1.00],
        [1.05, 1.05, 1.05],
    ])

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    voxel_cloud = voxelize_point_cloud(
        point_cloud,
        voxel_size=0.5,
    )

    assert not voxel_cloud.is_empty()
    assert len(voxel_cloud.points) < len(point_cloud.points)
def test_project_to_2_5d():
    points = np.array([
        [0.10, 0.10, 1.0],
        [0.20, 0.15, 2.0],
        [0.80, 0.80, 3.0],
        [1.10, 1.10, 4.0],
    ])

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    projection = project_to_2_5d(
        point_cloud,
        grid_size=0.5,
    )

    assert not projection.empty

    assert list(projection.columns) == [
        "grid_x",
        "grid_y",
        "height",
        "point_density",
        "elevation_variation",
    ]

    # The first two points belong to the same 0.5 m grid cell.
    first_cell = projection[
        (projection["grid_x"] == 0)
        & (projection["grid_y"] == 0)
    ]

    assert len(first_cell) == 1
    assert first_cell.iloc[0]["height"] == 2.0
    assert first_cell.iloc[0]["point_density"] == 2
    assert first_cell.iloc[0]["elevation_variation"] == 1.0
def test_run_lidar_pipeline(tmp_path):
    points = np.array([
        [0.00, 0.00, 1.0],
        [0.05, 0.05, 1.1],
        [0.10, 0.10, 1.2],
        [1.00, 1.00, 2.0],
        [1.05, 1.05, 2.1],
    ])

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    test_file = tmp_path / "pipeline_cloud.ply"
    o3d.io.write_point_cloud(str(test_file), point_cloud)

    voxelized_cloud, map_2_5d = run_lidar_pipeline(
        str(test_file),
        voxel_size=0.5,
        grid_size=0.5,
        nb_neighbors=2,
        std_ratio=2.0,
    )

    assert not voxelized_cloud.is_empty()
    assert not map_2_5d.empty

    assert list(map_2_5d.columns) == [
        "grid_x",
        "grid_y",
        "height",
        "point_density",
        "elevation_variation",
    ]