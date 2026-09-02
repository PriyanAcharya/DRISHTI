from detection.schemas import Detection

from geometry.distance import (
    calculate_distance_xy,
    calculate_distance_3d
)

from output.json_exporter import export_detections


def main():

    detections = []

    # -------------------------
    # CAR
    # -------------------------

    x = 10.0
    y = 2.0
    z = 0.8

    car = Detection(
        object_id=None,

        class_name="Car",
        confidence=0.95,

        x=x,
        y=y,
        z=z,

        length=4.2,
        width=1.8,
        height=1.6,

        heading=0.3,

        distance_xy=calculate_distance_xy(x, y),

        distance_3d=calculate_distance_3d(
            x, y, z
        ),

        frame_id="test_001",
        timestamp=0.0
    )

    detections.append(car)

    # -------------------------
    # PEDESTRIAN
    # -------------------------

    x = 6.0
    y = -1.5
    z = 0.9

    pedestrian = Detection(
        object_id=None,

        class_name="Pedestrian",
        confidence=0.91,

        x=x,
        y=y,
        z=z,

        length=0.7,
        width=0.6,
        height=1.7,

        heading=1.2,

        distance_xy=calculate_distance_xy(x, y),

        distance_3d=calculate_distance_3d(
            x, y, z
        ),

        frame_id="test_001",
        timestamp=0.0
    )

    detections.append(pedestrian)

    # -------------------------
    # EXPORT
    # -------------------------

    export_detections(
        detections=detections,

        output_path=(
            "data/output/"
            "test_detections.json"
        ),

        frame_id="test_001",

        timestamp=0.0
    )


if __name__ == "__main__":
    main()