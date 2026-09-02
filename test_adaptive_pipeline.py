from person2_detection.adaptive_pipeline import (
    AdaptiveDetectionPipeline
)


pipeline = AdaptiveDetectionPipeline()


# =========================================
# FRAME 1
# =========================================

frame_1 = {

    "pred_boxes": [

        # Pedestrian
        [
            10.0,
            2.0,
            0.0,
            0.8,
            0.6,
            1.7,
            0.0
        ],

        # Car
        [
            20.0,
            5.0,
            0.0,
            4.0,
            1.8,
            1.6,
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


# =========================================
# FRAME 2
# =========================================

frame_2 = {

    "pred_boxes": [

        # Pedestrian moved closer
        [
            6.0,
            2.0,
            0.0,
            0.8,
            0.6,
            1.7,
            0.0
        ],

        # Car almost static
        [
            20.5,
            5.0,
            0.0,
            4.0,
            1.8,
            1.6,
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


# =========================================
# PROCESS FRAME 1
# =========================================

print("\nFRAME 1")

detections_1 = pipeline.process_frame(
    frame_1,
    frame_id="frame_001"
)


for detection in detections_1:

    print(
        detection.object_id,
        "|",
        detection.class_name,
        "| Importance:",
        detection.importance_score,
        "| Risk:",
        detection.risk_level,
        "| Resolution:",
        detection.recommended_resolution
    )


# =========================================
# PROCESS FRAME 2
# =========================================

print("\nFRAME 2")

detections_2 = pipeline.process_frame(
    frame_2,
    frame_id="frame_002"
)


for detection in detections_2:

    print(
        detection.object_id,
        "|",
        detection.class_name,
        "| Importance:",
        detection.importance_score,
        "| Risk:",
        detection.risk_level,
        "| Resolution:",
        detection.recommended_resolution
    )