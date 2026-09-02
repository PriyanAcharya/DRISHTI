from person2_detection.adaptive_pipeline import (
    AdaptiveDetectionPipeline
)

from person2_detection.output.json_exporter import (
    save_detections_json
)


# ==========================================
# CREATE PIPELINE
# ==========================================

pipeline = AdaptiveDetectionPipeline()


# ==========================================
# DEFINE SIMULATED LIDAR FRAMES
# ==========================================

frames = [

    {
        "frame_id": "frame_001",

        "predictions": {

            "pred_boxes": [

                # Pedestrian - far away
                [
                    25.0, 2.0, 0.0,
                    0.8, 0.6, 1.7,
                    0.0
                ],

                # Car - relatively static
                [
                    15.0, 5.0, 0.0,
                    4.0, 1.8, 1.6,
                    0.0
                ]
            ],

            "pred_scores": [
                0.95,
                0.90
            ],

            "pred_labels": [
                2,
                1
            ]
        }
    },


    {
        "frame_id": "frame_002",

        "predictions": {

            "pred_boxes": [

                # Pedestrian moving closer
                [
                    18.0, 2.0, 0.0,
                    0.8, 0.6, 1.7,
                    0.0
                ],

                # Car almost static
                [
                    15.5, 5.0, 0.0,
                    4.0, 1.8, 1.6,
                    0.0
                ]
            ],

            "pred_scores": [
                0.96,
                0.91
            ],

            "pred_labels": [
                2,
                1
            ]
        }
    },


    {
        "frame_id": "frame_003",

        "predictions": {

            "pred_boxes": [

                # Pedestrian now very close
                [
                    7.0, 2.0, 0.0,
                    0.8, 0.6, 1.7,
                    0.0
                ],

                # Car starts moving
                [
                    12.0, 5.0, 0.0,
                    4.0, 1.8, 1.6,
                    0.0
                ]
            ],

            "pred_scores": [
                0.97,
                0.92
            ],

            "pred_labels": [
                2,
                1
            ]
        }
    }

]


# ==========================================
# PROCESS ALL FRAMES
# ==========================================

for frame in frames:

    frame_id = frame["frame_id"]

    predictions = frame["predictions"]

    print("\n")
    print("=" * 60)
    print("PROCESSING:", frame_id)
    print("=" * 60)

    detections = pipeline.process_frame(
        predictions,
        frame_id
    )


    for detection in detections:

        print(
            f"\nObject ID: {detection.object_id}"
        )

        print(
            f"Class: {detection.class_name}"
        )

        print(
            f"Position: "
            f"({detection.x}, "
            f"{detection.y}, "
            f"{detection.z})"
        )

        print(
            f"Distance: "
            f"{round(detection.distance_xy, 2)} m"
        )

        print(
            f"Importance Score: "
            f"{detection.importance_score}"
        )
        print(
            f"Motion Score: "
            f"{detection.motion_score}"
       )
        print(
            f"Risk Level: "
            f"{detection.risk_level}"
        )

        print(
            f"Recommended Resolution: "
            f"{detection.recommended_resolution}"
        )


    # Save each frame output
    save_detections_json(
        detections,
        frame_id,
        f"{frame_id}_output.json"
    )