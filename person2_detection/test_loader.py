import numpy as np

from data_loader.validator import validate_point_cloud
from preprocessing.preprocess import preprocess_point_cloud


def main():

    # Create a simulated LiDAR point cloud
    # 1000 points with XYZ + intensity

    points = np.random.uniform(
        low=-60,
        high=60,
        size=(1000, 4)
    ).astype(np.float32)

    print("Raw point cloud shape:")
    print(points.shape)

    # Validation
    validated_points = validate_point_cloud(points)

    print("\nAfter validation:")
    print(validated_points.shape)

    # Preprocessing
    processed_points = preprocess_point_cloud(
        validated_points
    )

    print("\nAfter preprocessing:")
    print(processed_points.shape)

    print("\nPoint cloud pipeline successful!")


if __name__ == "__main__":
    main()