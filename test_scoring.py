from person2_detection.scoring.importance import score_detection


test_objects = [
    {
        "class_name": "Pedestrian",
        "distance": 4.0,
        "confidence": 0.95,
        "motion_score": 0.8
    },
    {
        "class_name": "Car",
        "distance": 18.0,
        "confidence": 0.88,
        "motion_score": 0.4
    },
    {
        "class_name": "Truck",
        "distance": 50.0,
        "confidence": 0.75,
        "motion_score": 0.1
    }
]


for obj in test_objects:

    result = score_detection(
        class_name=obj["class_name"],
        distance=obj["distance"],
        confidence=obj["confidence"],
        motion_score=obj["motion_score"]
    )

    print("\nObject:", obj["class_name"])
    print("Distance:", obj["distance"], "m")
    print("Confidence:", obj["confidence"])

    print("Importance Score:",
          result["importance_score"])

    print("Risk Level:",
          result["risk_level"])

    print("Recommended Resolution:",
          result["recommended_resolution"])