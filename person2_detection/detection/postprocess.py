from datetime import datetime

from person2_detection.detection.schemas import Detection
from person2_detection.geometry.distance import (
    calculate_distance_xy,
    calculate_distance_3d
)
from person2_detection.scoring.importance import score_detection


# KITTI / PointPillars label mapping
LABEL_MAP = {
    1: "Car",
    2: "Pedestrian",
    3: "Cyclist"
}


def postprocess_predictions(predictions, frame_id="unknown"):
    """
    Convert raw 3D detector predictions into Detection objects.

    Expected prediction format:

    predictions = {
        "pred_boxes": [
            [x, y, z, length, width, height, heading]
        ],
        "pred_scores": [
            confidence
        ],
        "pred_labels": [
            class_label
        ]
    }

    Returns:
        list[Detection]
    """

    detections = []

    pred_boxes = predictions.get("pred_boxes", [])
    pred_scores = predictions.get("pred_scores", [])
    pred_labels = predictions.get("pred_labels", [])

    # Ensure all prediction arrays have matching lengths
    num_predictions = min(
        len(pred_boxes),
        len(pred_scores),
        len(pred_labels)
    )

    timestamp = datetime.now().timestamp()

    for i in range(num_predictions):

        # Extract 3D bounding box
        box = pred_boxes[i]

        if len(box) < 7:
            continue

        x = float(box[0])
        y = float(box[1])
        z = float(box[2])

        length = float(box[3])
        width = float(box[4])
        height = float(box[5])

        heading = float(box[6])

        # Detection confidence
        confidence = float(pred_scores[i])

        # Object label
        label = int(pred_labels[i])

        class_name = LABEL_MAP.get(
            label,
            "Unknown"
        )

        # Calculate object distances
        distance_xy = calculate_distance_xy(
            x,
            y
        )

        distance_3d = calculate_distance_3d(
            x,
            y,
            z
        )

        # Calculate adaptive importance information
        scoring_result = score_detection(
            class_name=class_name,
            distance=distance_xy,
            confidence=confidence,
            motion_score=0.0
        )

        # Create standardized detection object
        detection = Detection(
            object_id=f"{frame_id}_{i}",

            class_name=class_name,
            confidence=confidence,

            x=x,
            y=y,
            z=z,

            length=length,
            width=width,
            height=height,

            heading=heading,

            distance_xy=distance_xy,
            distance_3d=distance_3d,

            importance_score=scoring_result[
                "importance_score"
            ],

            risk_level=scoring_result[
                "risk_level"
            ],

            recommended_resolution=scoring_result[
                "recommended_resolution"
            ],

            frame_id=frame_id,
            timestamp=timestamp
        )

        detections.append(
            detection
        )

    return detections