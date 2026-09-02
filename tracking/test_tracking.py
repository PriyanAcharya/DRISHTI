from tracking.tracker import ObjectTracker
from tracking.motion import MotionAnalyzer


def test_tracker_assigns_id():
    tracker = ObjectTracker()

    detections = [
        {
            "label": "Car",
            "position": (10.0, 5.0)
        }
    ]

    result = tracker.update(detections)

    assert len(result) == 1
    assert result[0]["id"] == 1
    assert result[0]["label"] == "Car"
    assert result[0]["position"] == (10.0, 5.0)


def test_tracker_preserves_id_for_same_label():
    tracker = ObjectTracker()

    first_frame = [
        {
            "label": "Car",
            "position": (10.0, 5.0)
        }
    ]

    second_frame = [
        {
            "label": "Car",
            "position": (11.0, 5.0)
        }
    ]

    first_result = tracker.update(first_frame)
    second_result = tracker.update(second_frame)

    assert first_result[0]["id"] == second_result[0]["id"]


def test_tracker_stores_position_history():
    tracker = ObjectTracker(history_size=3)

    tracker.update([
        {
            "label": "Car",
            "position": (10.0, 5.0)
        }
    ])

    result = tracker.update([
        {
            "label": "Car",
            "position": (11.0, 5.0)
        }
    ])

    assert result[0]["position_history"] == [
        (10.0, 5.0),
        (11.0, 5.0)
    ]


def test_motion_velocity():
    motion = MotionAnalyzer()

    velocity = motion.calculate_velocity(
        (10.0, 5.0),
        (10.5, 5.0),
        dt=0.1
    )

    assert velocity == (5.0, 0.0)


def test_motion_speed():
    motion = MotionAnalyzer()

    speed = motion.calculate_speed(
        (3.0, 4.0)
    )

    assert speed == 5.0


def test_motion_direction():
    motion = MotionAnalyzer()

    assert motion.calculate_direction((1.0, 1.0)) == "UP_RIGHT"
    assert motion.calculate_direction((-1.0, 1.0)) == "UP_LEFT"
    assert motion.calculate_direction((1.0, -1.0)) == "DOWN_RIGHT"
    assert motion.calculate_direction((-1.0, -1.0)) == "DOWN_LEFT"
    assert motion.calculate_direction((0.0, 0.0)) == "STATIONARY"


def test_motion_prediction():
    motion = MotionAnalyzer()

    predicted = motion.predict_position(
        (10.0, 5.0),
        (5.0, 0.0),
        prediction_time=1.0
    )

    assert predicted == (15.0, 5.0)