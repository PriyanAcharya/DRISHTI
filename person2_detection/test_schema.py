from detection.schemas import Detection
from geometry.distance import (
    calculate_distance_xy,
    calculate_distance_3d
)


def main():
    x = 10.0
    y = 5.0
    z = 1.0

    distance_xy = calculate_distance_xy(x, y)
    distance_3d = calculate_distance_3d(x, y, z)

    detection = Detection(
        object_id=None,
        class_name="Car",
        confidence=0.95,

        x=x,
        y=y,
        z=z,

        length=4.2,
        width=1.8,
        height=1.6,

        heading=0.5,

        distance_xy=distance_xy,
        distance_3d=distance_3d,

        frame_id="test_001",
        timestamp=0.0
    )

    print("Detection Object:\n")
    print(detection)

    print("\nJSON-ready output:\n")
    print(detection.to_dict())


if __name__ == "__main__":
    main()