import json


def detections_to_dict(
    detections,
    frame_id
):
    """
    Convert Detection objects into a clean dictionary.
    """

    output = {
        "frame_id": frame_id,
        "detections": []
    }

    for detection in detections:

        detection_data = {

            "object_id":
                detection.object_id,

            "class_name":
                detection.class_name,

            "confidence":
                detection.confidence,

            "position": {
                "x": detection.x,
                "y": detection.y,
                "z": detection.z
            },

            "dimensions": {
                "length": detection.length,
                "width": detection.width,
                "height": detection.height
            },

            "heading":
                detection.heading,

            "distance": {
                "xy":
                    detection.distance_xy,

                "3d":
                    detection.distance_3d
            },

            "importance_score":
                detection.importance_score,
            "motion_score":
                detection.motion_score,
            "risk_level":
                detection.risk_level,

            "recommended_resolution":
                detection.recommended_resolution
        }

        output["detections"].append(
            detection_data
        )

    return output


# =========================================
# SAVE DETECTIONS AS JSON
# =========================================

def save_detections_json(
    detections,
    frame_id,
    filename
):

    data = detections_to_dict(
        detections,
        frame_id
    )

    with open(filename, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )

    print(
        f"Detection output saved to {filename}"
    )