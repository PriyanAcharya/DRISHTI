from person2_detection.tracking.motion_estimator import (
    MotionEstimator
)


motion_estimator = MotionEstimator()


# Frame 1
score_1 = motion_estimator.calculate_motion(
    object_id="car_1",
    x=10.0,
    y=5.0,
    z=0.0
)

print("Frame 1 Motion Score:", score_1)


# Frame 2
score_2 = motion_estimator.calculate_motion(
    object_id="car_1",
    x=12.0,
    y=5.0,
    z=0.0
)

print("Frame 2 Motion Score:", score_2)


# Frame 3
score_3 = motion_estimator.calculate_motion(
    object_id="car_1",
    x=16.0,
    y=5.0,
    z=0.0
)

print("Frame 3 Motion Score:", score_3)