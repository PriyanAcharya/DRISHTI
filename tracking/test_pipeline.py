from tracking.pipeline import TrackingRiskPipeline
from person2_detection.detection.schemas import Detection


def make_detection(object_id, x, timestamp):
    return Detection(
        object_id=object_id,
        class_name="Car",
        confidence=0.95,
        x=x,
        y=0.0,
        z=0.0,
        length=4.0,
        width=2.0,
        height=1.5,
        heading=0.0,
        distance_xy=abs(x),
        distance_3d=abs(x),
        timestamp=timestamp
    )


def test_first_detection_is_stationary():
    pipeline = TrackingRiskPipeline()

    detection = make_detection(
        "track_1",
        10.0,
        100.0
    )

    result = pipeline.process_detection(detection)

    assert result["id"] == "track_1"
    assert result["speed"] == 0.0
    assert result["direction"] == "STATIONARY"
    assert result["risk_level"] == "LOW"


def test_velocity_uses_timestamp_difference():
    pipeline = TrackingRiskPipeline()

    detection1 = make_detection(
        "track_1",
        10.0,
        100.0
    )

    detection2 = make_detection(
        "track_1",
        9.0,
        100.5
    )

    pipeline.process_detection(detection1)
    result = pipeline.process_detection(detection2)

    assert result["dt"] == 0.5
    assert result["vx"] == -2.0
    assert result["speed"] == 2.0
    assert result["direction"] == "LEFT"


def test_approaching_object_has_collision_risk():
    pipeline = TrackingRiskPipeline()

    detection1 = make_detection(
        "track_1",
        10.0,
        100.0
    )

    detection2 = make_detection(
        "track_1",
        9.0,
        100.5
    )

    pipeline.process_detection(detection1)
    result = pipeline.process_detection(detection2)

    assert result["closing_speed"] > 0
    assert result["ttc"] < float("inf")
    assert result["risk_level"] in ("MEDIUM", "HIGH")


def test_object_moving_away_has_no_collision_ttc():
    pipeline = TrackingRiskPipeline()

    detection1 = make_detection(
        "track_1",
        9.0,
        100.0
    )

    detection2 = make_detection(
        "track_1",
        10.0,
        100.5
    )

    pipeline.process_detection(detection1)
    result = pipeline.process_detection(detection2)

    assert result["vx"] == 2.0
    assert result["direction"] == "RIGHT"
    assert result["closing_speed"] == 0.0
    assert result["ttc"] == float("inf")
    assert result["risk_level"] == "LOW"


def test_prediction_trajectory_is_generated():
    pipeline = TrackingRiskPipeline(
        prediction_horizon=1.0,
        prediction_step=0.5
    )

    detection1 = make_detection(
        "track_1",
        10.0,
        100.0
    )

    detection2 = make_detection(
        "track_1",
        9.0,
        100.5
    )

    pipeline.process_detection(detection1)
    result = pipeline.process_detection(detection2)

    trajectory = result["trajectory"]

    assert len(trajectory) == 3
    assert trajectory[0]["x"] == 9.0
    assert trajectory[1]["x"] == 8.0
    assert trajectory[2]["x"] == 7.0