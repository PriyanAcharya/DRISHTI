from tracker import ObjectTracker
from motion import MotionAnalyzer
from risk import RiskAnalyzer


def test_tracking_pipeline():

    tracker = ObjectTracker()
    motion = MotionAnalyzer()
    risk = RiskAnalyzer()

    # -------------------------
    # Frame 1
    # -------------------------
    frame1 = [
        {
            "label": "person",
            "position": (10, 5)
        }
    ]

    tracked_frame1 = tracker.update(frame1)

    # -------------------------
    # Frame 2
    # -------------------------
    frame2 = [
        {
            "label": "person",
            "position": (13, 7)
        }
    ]

    tracked_frame2 = tracker.update(frame2)

    # -------------------------
    # Frame 3
    # -------------------------
    frame3 = [
        {
            "label": "person",
            "position": (16, 9)
        }
    ]

    tracked_frame3 = tracker.update(frame3)

    # -------------------------
    # Motion Analysis
    # -------------------------

    previous_position = tracked_frame2[0]["position"]
    current_position = tracked_frame3[0]["position"]

    velocity = motion.calculate_velocity(
        previous_position,
        current_position
    )

    speed = motion.calculate_speed(
        velocity
    )

    direction = motion.calculate_direction(
        velocity
    )

    predicted_position = motion.predict_position(
        current_position,
        velocity
    )

    # -------------------------
    # Risk Analysis
    # -------------------------

    distance = 4

    time_to_collision = risk.calculate_time_to_collision(
        distance,
        velocity
    )

    risk_level = risk.calculate_risk(
        distance,
        velocity
    )

    # -------------------------
    # Display Results
    # -------------------------

    print("=== Tracking Pipeline Test ===")

    print("\nFrame 1:")
    print(tracked_frame1)

    print("\nFrame 2:")
    print(tracked_frame2)

    print("\nFrame 3:")
    print(tracked_frame3)

    print("\n--- Motion Analysis ---")
    print("Velocity:", velocity)
    print("Speed:", round(speed, 2))
    print("Direction:", direction)
    print("Predicted Position:", predicted_position)

    print("\n--- Risk Analysis ---")
    print("Distance:", distance)
    print(
        "Time to Collision:",
        round(time_to_collision, 2)
    )
    print("Risk Level:", risk_level)


if __name__ == "__main__":
    test_tracking_pipeline()