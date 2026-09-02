from person2_detection.adaptive_pipeline import (
    AdaptiveDetectionPipeline
)

from person2_detection.output.json_exporter import (
    save_detections_json
)


# Create pipeline
pipeline = AdaptiveDetectionPipeline()


# Sample LiDAR detection predictions
predictions = {

    "pred_boxes": [

        # Pedestrian
        [
            6.0,
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
        0.96,
        0.91
    ],

    "pred_labels": [
        2,
        1
    ]
}


# Frame identifier
frame_id = "frame_001"


# Process detections
detections = pipeline.process_frame(
    predictions,
    frame_id
)


# Save output as JSON
save_detections_json(
    detections,
    frame_id,
    "person2_output.json"
)