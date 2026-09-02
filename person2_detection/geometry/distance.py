import math


def calculate_distance_xy(x: float, y: float) -> float:
    """
    Calculate horizontal distance from the LiDAR sensor.

    Formula:
        sqrt(x² + y²)
    """

    return math.sqrt(x ** 2 + y ** 2)


def calculate_distance_3d(
    x: float,
    y: float,
    z: float
) -> float:
    """
    Calculate full 3D Euclidean distance from the LiDAR sensor.

    Formula:
        sqrt(x² + y² + z²)
    """

    return math.sqrt(
        x ** 2 +
        y ** 2 +
        z ** 2
    )
