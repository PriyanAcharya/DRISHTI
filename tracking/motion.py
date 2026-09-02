class MotionAnalyzer:
    """
    Analyzes object movement using position history.

    Calculates:
    - Velocity
    - Direction
    - Predicted future position
    """

    def calculate_velocity(self, previous_position, current_position):
        """
        Calculate movement between two positions.
        """

        previous_x, previous_y = previous_position
        current_x, current_y = current_position

        velocity_x = current_x - previous_x
        velocity_y = current_y - previous_y

        return velocity_x, velocity_y

    def calculate_speed(self, velocity):
        """
        Calculate the speed from velocity.
        """

        velocity_x, velocity_y = velocity

        speed = (velocity_x ** 2 + velocity_y ** 2) ** 0.5

        return round(speed, 2)

    def calculate_direction(self, velocity):
        """
        Determine the basic movement direction.
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

    def predict_position(self, current_position, velocity, steps=1):
        """
        Predict the future position using current velocity.
        """

        current_x, current_y = current_position
        velocity_x, velocity_y = velocity

        predicted_x = current_x + (velocity_x * steps)
        predicted_y = current_y + (velocity_y * steps)

        return predicted_x, predicted_y


# Simple test
if __name__ == "__main__":

    motion = MotionAnalyzer()

    previous_position = (13, 7)
    current_position = (16, 9)

    velocity = motion.calculate_velocity(
        previous_position,
        current_position
    )

    speed = motion.calculate_speed(velocity)

    direction = motion.calculate_direction(velocity)

    predicted_position = motion.predict_position(
        current_position,
        velocity
    )

    print("Previous Position:", previous_position)
    print("Current Position:", current_position)
    print("Velocity:", velocity)
    print("Speed:", speed)
    print("Direction:", direction)
    print("Predicted Position:", predicted_position)