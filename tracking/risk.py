import math


class RiskAnalyzer:
    """
    Analyzes object risk using:
    - Distance
    - Velocity
    - Speed
    - Time-to-collision

    This is a prototype risk model for DRISHTI.
    """

    def calculate_speed(self, velocity):
        """
        Calculate speed from velocity.
        """

        velocity_x, velocity_y = velocity

        speed = math.sqrt(
            velocity_x ** 2 + velocity_y ** 2
        )

        return speed

    def calculate_time_to_collision(self, distance, velocity):
        """
        Estimate time-to-collision.

        This is a simplified prototype calculation.
        It assumes the object is moving toward
        the critical area.

        Returns:
            float: Estimated time-to-collision.
        """

        speed = self.calculate_speed(velocity)

        if speed == 0:
            return float("inf")

        return distance / speed

    def calculate_risk(self, distance, velocity):
        """
        Calculate risk using distance, speed,
        and estimated time-to-collision.

        Risk levels:
            HIGH
            MEDIUM
            LOW
        """

        speed = self.calculate_speed(velocity)

        time_to_collision = self.calculate_time_to_collision(
            distance,
            velocity
        )

        # High risk:
        # Object is close and moving quickly,
        # or estimated collision time is very short.
        if (
            time_to_collision <= 2
            or (distance < 5 and speed > 2)
        ):
            return "HIGH"

        # Medium risk:
        # Object is moderately close or has
        # a relatively short collision time.
        elif (
            time_to_collision <= 5
            or (distance < 10 and speed > 1)
        ):
            return "MEDIUM"

        # Otherwise the risk is low.
        else:
            return "LOW"


# Simple test
if __name__ == "__main__":

    risk = RiskAnalyzer()

    distance = 4
    velocity = (3, 2)

    speed = risk.calculate_speed(
        velocity
    )

    time_to_collision = risk.calculate_time_to_collision(
        distance,
        velocity
    )

    risk_level = risk.calculate_risk(
        distance,
        velocity
    )

    print("Distance:", distance)
    print("Velocity:", velocity)
    print("Speed:", round(speed, 2))
    print(
        "Time to Collision:",
        round(time_to_collision, 2)
    )
    print("Risk Level:", risk_level)