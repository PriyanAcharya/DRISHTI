import time

from data_loader.loader import load_point_cloud
from data_loader.validator import validate_point_cloud

from preprocessing.preprocess import (
    preprocess_point_cloud
)


def process_point_cloud(
    file_path: str
):
    """
    Person 2 LiDAR processing pipeline.

    Steps:

    Load
        ↓
    Validate
        ↓
    Preprocess
        ↓
    Return detector-ready points
    """

    # -------------------------
    # LOAD
    # -------------------------

    points = load_point_cloud(
        file_path
    )

    print(
        f"Loaded points: {points.shape}"
    )

    # -------------------------
    # VALIDATE
    # -------------------------

    points = validate_point_cloud(
        points
    )

    print(
        f"Validated points: {points.shape}"
    )

    # -------------------------
    # PREPROCESS
    # -------------------------

    points = preprocess_point_cloud(
        points
    )

    print(
        f"Processed points: {points.shape}"
    )

    return points


if __name__ == "__main__":

    print(
        "Person 2 LiDAR Detection Pipeline Ready"
    )