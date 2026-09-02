import numpy as np

from detection.postprocess import (
    convert_predictions_to_detections
)


def main():

    # Simulated PointPillars output
    # Format:
    # [x, y, z, dx, dy, dz, heading]

    pred_boxes = np.array([
        [
            12.4,
            -2.3,
            0.8,
            4.2,
            1.8,
            1.6,
            1.57
        ],

        [
            6.2,
            1.5,
            0.9,
            0.7,
            0.6,
            1.7,
            0.20
        ],

        [
            18.0,
            -3.0,
            1.0,
            1.8,
            0.6,
            1.5,
            0.90
        ]
    ], dtype=np.float32)

    pred_scores = np.array([
        0.95,
        0.91,
        0.87
    ], dtype=np.float32)

    pred_labels = np.array([
        1,  # Car
        2,  # Pedestrian
        3   # Cyclist
    ], dtype=np.int32)

    detections = convert_predictions_to_detections(
        pred_boxes=pred_boxes,
        pred_scores=pred_scores,
        pred_labels=pred_labels,

        frame_id="test_frame_001",
        timestamp=0.0,

        confidence_threshold=0.30
    )

    print("\nDETECTIONS\n")
    print("-" * 50)

    for detection in detections:

        print(
            detection.to_dict()
        )

        print("-" * 50)

    print(
        f"\nTotal detections: {len(detections)}"
    )


if __name__ == "__main__":
    main()