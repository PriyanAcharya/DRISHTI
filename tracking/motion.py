class MotionAnalyzer:
    """
    Analyzes object movement using position history.

    Calculates:
    - Velocity in meters/second
    - Speed
    - Direction
    - Predicted future position
    """

    def calculate_velocity(
        self,
        previous_position,
        current_position,
        dt=0.1
    ):
        """
        Calculate velocity in meters/second.

        Parameters:
            previous_position: (x, y)
            current_position: (x, y)
            dt: time between frames in seconds
        """

        if dt <= 0:
            raise ValueError("dt must be greater than 0")

        previous_x, previous_y = previous_position
        current_x, current_y = current_position

        velocity_x = (
            current_x - previous_x
        ) / dt

        velocity_y = (
            current_y - previous_y
        ) / dt

        return velocity_x, velocity_y

    def calculate_speed(self, velocity):
        """
        Calculate speed from velocity.
        """

        velocity_x, velocity_y = velocity

        speed = (
            velocity_x ** 2 +
            velocity_y ** 2
        ) ** 0.5

        return round(speed, 2)

    def calculate_direction(self, velocity):
        """
        Determine basic movement direction.
        """

        velocity_x, velocity_y = velocity

        if velocity_x == 0 and velocity_y == 0:
            return "STATIONARY"

        if velocity_x > 0 and velocity_y > 0:
            return "UP_RIGHT"

        if velocity_x < 0 and velocity_y > 0:
            return "UP_LEFT"

        if velocity_x > 0 and velocity_y < 0:
            return "DOWN_RIGHT"

        if velocity_x < 0 and velocity_y < 0:
            return "DOWN_LEFT"

        if velocity_x > 0:
            return "RIGHT"

        if velocity_x < 0:
            return "LEFT"

        if velocity_y > 0:
            return "UP"

        return "DOWN"

    def predict_position(
        self,
        current_position,
        velocity,
        prediction_time=1.0
    ):
        """
        Predict future XY position using
        constant-velocity motion.

        prediction_time:
            Future time in seconds.
        """

        current_x, current_y = current_position
        velocity_x, velocity_y = velocity

        predicted_x = (
            current_x +
            velocity_x * prediction_time
        )

        predicted_y = (
            current_y +
            velocity_y * prediction_time
        )

        return predicted_x, predicted_y