from person2_detection.detection.postprocess import (
    postprocess_predictions
)


predictions = {
    "pred_boxes": [
        # Pedestrian
        [4.0, 1.5, 0.8, 0.8, 0.6, 1.7, 0.1],

        # Car
        [15.0, -2.0, 1.0, 4.2, 1.8, 1.6, 0.0],

        # Cyclist
        [45.0, 8.0, 1.5, 1.8, 0.7, 1.6, 0.2]
    ],

    "pred_scores": [
        0.95,
        0.88,
        0.78
    ],

    "pred_labels": [
        2,
        1,
        3
    ]
}


detections = postprocess_predictions(
    predictions,
    frame_id="test_frame_001"
)


for detection in detections:

    print("\n" + "=" * 40)

    print("Object ID:",
          detection.object_id)

    print("Class:",
          detection.class_name)

    print("Confidence:",
          detection.confidence)

    print("Position:",
          f"({detection.x}, "
          f"{detection.y}, "
          f"{detection.z})")

    print("Distance XY:",
          detection.distance_xy,
          "m")

    print("Distance 3D:",
          detection.distance_3d,
          "m")

    print("\nADAPTIVE MAPPING")

    print("Importance Score:",
          detection.importance_score)

    print("Risk Level:",
          detection.risk_level)

    print("Recommended Resolution:",
          detection.recommended_resolution)