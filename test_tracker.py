from person2_detection.detection.schemas import Detection
from person2_detection.tracking.object_tracker import (
    ObjectTracker
)


tracker = ObjectTracker()


# Frame 1
frame_1 = [

    Detection(
        object_id="temp_1",
        class_name="Car",
        confidence=0.9,

        x=10.0,
        y=5.0,
        z=0.0,

        length=4.0,
        width=1.8,
        height=1.5,

        heading=0.0,

        distance_xy=11.18,
        distance_3d=11.18,

        frame_id="frame_1",
        timestamp=0.0
    )

]


# Track Frame 1
frame_1 = tracker.update(
    frame_1
)


print(
    "Frame 1 ID:",
    frame_1[0].object_id
)


# Frame 2
frame_2 = [

    Detection(
        object_id="temp_2",
        class_name="Car",
        confidence=0.9,

        x=12.0,
        y=5.0,
        z=0.0,

        length=4.0,
        width=1.8,
        height=1.5,

        heading=0.0,

        distance_xy=13.0,
        distance_3d=13.0,

        frame_id="frame_2",
        timestamp=1.0
    )

]


# Track Frame 2
frame_2 = tracker.update(
    frame_2
)


print(
    "Frame 2 ID:",
    frame_2[0].object_id
)