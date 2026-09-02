from .motion import MotionAnalyzer
from .prediction import predict_trajectory
from .risk import RiskAnalyzer


class TrackingRiskPipeline:
    """
    Person 4 tracking, prediction, and risk pipeline.

    Adds:
    - velocity
    - speed
    - direction
    - predicted trajectory
    - closing speed
    - time-to-collision (TTC)
    - risk score
    - risk level
    """

    def __init__(
        self,
        dt=0.1,
        prediction_horizon=3.0,
        prediction_step=0.25
    ):
        self.motion = MotionAnalyzer()
        self.risk = RiskAnalyzer()

        self.dt = dt
        self.prediction_horizon = prediction_horizon
        self.prediction_step = prediction_step

        # Previous position and timestamp for each tracked object.
        self.previous_positions = {}
        self.previous_timestamps = {}

    def process_object(self, obj, previous_position, dt=None):
        """
        Process one tracked object.

        Expected obj:
            {
                "id": ...,
                "x": ...,
                "y": ...,
                "z": ...
            }

        previous_position:
            (previous_x, previous_y)

        dt:
            Time difference between frames in seconds.
        """

        current_position = (
            obj["x"],
            obj["y"]
        )

        if dt is None:
            dt = self.dt

        velocity = self.motion.calculate_velocity(
            previous_position,
            current_position,
            dt
        )

        speed = self.motion.calculate_speed(velocity)
        direction = self.motion.calculate_direction(velocity)

        prediction_object = {
            "x": obj["x"],
            "y": obj["y"],
            "z": obj.get("z", 0.0),
            "vx": velocity[0],
            "vy": velocity[1]
        }

        trajectory = predict_trajectory(
            prediction_object,
            horizon=self.prediction_horizon,
            step=self.prediction_step
        )

        distance = (
            obj["x"] ** 2 +
            obj["y"] ** 2
        ) ** 0.5

        risk = self.risk.calculate_risk(
            distance=distance,
            velocity=velocity,
            position=current_position
        )

        return {
            "id": obj.get("id"),
            "x": obj["x"],
            "y": obj["y"],
            "z": obj.get("z", 0.0),
            "vx": velocity[0],
            "vy": velocity[1],
            "speed": speed,
            "direction": direction,
            "trajectory": trajectory,
            "distance": risk["distance"],
            "closing_speed": risk["closing_speed"],
            "ttc": risk["ttc"],
            "risk_score": risk["risk_score"],
            "risk_level": risk["risk_level"]
        }

    def process_detection(self, detection, previous_position=None):
        """
        Process a Person 2 Detection object.

        Uses timestamp differences when available.
        Falls back to self.dt when timestamps are missing
        or invalid.
        """

        object_id = detection.object_id

        current_position = (
            detection.x,
            detection.y
        )

        previous_timestamp = self.previous_timestamps.get(
            object_id
        )

        current_timestamp = detection.timestamp

        # Use the timestamp difference when both timestamps
        # are valid and the difference is positive.
        if (
            previous_timestamp is not None
            and current_timestamp > previous_timestamp
        ):
            dt = current_timestamp - previous_timestamp
        else:
            dt = self.dt

        # If the caller explicitly supplied a previous position,
        # use it. Otherwise use the stored position.
        if previous_position is None:
            previous_position = self.previous_positions.get(
                object_id
            )

        # Store current state for the next frame.
        self.previous_positions[object_id] = current_position
        self.previous_timestamps[object_id] = current_timestamp

        # First observation: no velocity can be calculated yet.
        if previous_position is None:
            return {
                "id": object_id,
                "x": detection.x,
                "y": detection.y,
                "z": detection.z,
                "vx": 0.0,
                "vy": 0.0,
                "speed": 0.0,
                "direction": "STATIONARY",
                "trajectory": [
                    {
                        "x": detection.x,
                        "y": detection.y,
                        "z": detection.z,
                        "time": 0.0
                    }
                ],
                "distance": detection.distance_xy,
                "closing_speed": 0.0,
                "ttc": float("inf"),
                "risk_score": 0.0,
                "risk_level": "LOW",
                "class_name": detection.class_name,
                "confidence": detection.confidence,
                "frame_id": detection.frame_id,
                "timestamp": detection.timestamp,
                "dt": 0.0
            }

        obj = {
            "id": object_id,
            "x": detection.x,
            "y": detection.y,
            "z": detection.z
        }

        result = self.process_object(
            obj,
            previous_position,
            dt=dt
        )

        # Preserve Person 2 information.
        result["class_name"] = detection.class_name
        result["confidence"] = detection.confidence
        result["frame_id"] = detection.frame_id
        result["timestamp"] = detection.timestamp
        result["dt"] = dt

        return result