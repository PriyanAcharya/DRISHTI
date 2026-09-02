import math


# Importance weights for different detected objects
CLASS_WEIGHTS = {
    "Pedestrian": 1.0,
    "Cyclist": 0.9,
    "Car": 0.8,
    "Truck": 0.85,
    "Bus": 0.85,
    "Motorcycle": 0.9,
    "Unknown": 0.5,
}


def calculate_distance_score(distance):
    """
    Convert object distance into an importance score.

    Closer objects receive a higher score.
    Output range: 0.0 to 1.0
    """

    if distance <= 0:
        return 1.0

    # Objects within 5 m are highly important
    if distance <= 5:
        return 1.0

    # Objects beyond 60 m have low importance
    if distance >= 60:
        return 0.1

    # Smooth decrease in importance with distance
    score = 1 - ((distance - 5) / 55)

    return max(0.1, min(score, 1.0))


def calculate_importance_score(
    class_name,
    distance,
    confidence,
    motion_score=0.0
):
    """
    Calculate the adaptive importance score.

    Parameters
    ----------
    class_name : str
        Detected object class

    distance : float
        Distance from LiDAR sensor in meters

    confidence : float
        Detection confidence from the 3D detector

    motion_score : float
        Optional motion importance score (0 to 1)

    Returns
    -------
    float
        Importance score between 0 and 1
    """

    distance_score = calculate_distance_score(distance)

    class_score = CLASS_WEIGHTS.get(
        class_name,
        CLASS_WEIGHTS["Unknown"]
    )

    confidence_score = max(0.0, min(confidence, 1.0))

    motion_score = max(0.0, min(motion_score, 1.0))

    # Weighted importance formula
    importance = (
        0.40 * distance_score +
        0.25 * class_score +
        0.20 * confidence_score +
        0.15 * motion_score
    )

    return round(
        max(0.0, min(importance, 1.0)),
        3
    )


def get_resolution_level(importance_score):
    """
    Convert importance into adaptive map resolution.
    """

    if importance_score >= 0.80:
        return "HIGH"

    elif importance_score >= 0.50:
        return "MEDIUM"

    return "LOW"


def get_risk_level(class_name, distance):
    """
    Determine risk based on object type and distance.
    """

    # High-priority vulnerable objects
    vulnerable_objects = [
        "Pedestrian",
        "Cyclist",
        "Motorcycle"
    ]

    if class_name in vulnerable_objects:

        if distance <= 10:
            return "HIGH"

        elif distance <= 25:
            return "MEDIUM"

        return "LOW"

    # Vehicles and other objects
    if distance <= 8:
        return "HIGH"

    elif distance <= 20:
        return "MEDIUM"

    return "LOW"


def score_detection(
    class_name,
    distance,
    confidence,
    motion_score=0.0
):
    """
    Complete scoring pipeline.

    Returns importance, risk and resolution recommendation.
    """

    importance_score = calculate_importance_score(
        class_name=class_name,
        distance=distance,
        confidence=confidence,
        motion_score=motion_score
    )

    risk_level = get_risk_level(
        class_name=class_name,
        distance=distance
    )

    resolution_level = get_resolution_level(
        importance_score
    )

    return {
        "importance_score": importance_score,
        "risk_level": risk_level,
        "recommended_resolution": resolution_level
    }