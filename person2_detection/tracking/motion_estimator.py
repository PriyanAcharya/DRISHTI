import math


class MotionEstimator:
    """
    Estimates object motion by comparing object
    positions between consecutive LiDAR frames.
    """

    def __init__(self):

        # Stores previous object positions
        self.previous_positions = {}

    def calculate_motion(
        self,
        object_id,
        x,
        y,
        z
    ):
        """
        Calculate normalized motion score.

        Returns:
            motion_score between 0.0 and 1.0
        """

        current_position = (
            x,
            y,
            z
        )

        # First time seeing object
        if object_id not in self.previous_positions:

            self.previous_positions[
                object_id
            ] = current_position

            return 0.0

        previous_position = (
            self.previous_positions[
                object_id
            ]
        )

        # Calculate displacement
        dx = (
            x -
            previous_position[0]
        )

        dy = (
            y -
            previous_position[1]
        )

        dz = (
            z -
            previous_position[2]
        )

        displacement = math.sqrt(
            dx ** 2 +
            dy ** 2 +
            dz ** 2
        )

        # Update stored position
        self.previous_positions[
            object_id
        ] = current_position

        # Normalize displacement
        # 5 meters/frame or above = maximum motion score

        motion_score = min(
            displacement / 5.0,
            1.0
        )

        return round(
            motion_score,
            3
        )