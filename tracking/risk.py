import math


class RiskAnalyzer:
    """
    Analyzes dynamic object risk using:
    - Distance
    - Velocity
    - Closing speed
    - Time-to-collision
    - Risk score
    """

    def calculate_speed(self, velocity):
        """
        Calculate speed from XY velocity.
        """

        velocity_x, velocity_y = velocity

        return math.sqrt(
            velocity_x ** 2 +
            velocity_y ** 2
        )

    def calculate_closing_speed(
        self,
        position,
        velocity
    ):
        """
        Calculate how quickly an object is approaching
        the LiDAR sensor/reference point.

        Positive value:
            Object is approaching.

        Zero or negative:
            Object is not approaching.
        """

        x, y = position
        velocity_x, velocity_y = velocity

        distance = math.sqrt(
            x ** 2 +
            y ** 2
        )

        if distance == 0:
            return 0.0

        # Unit vector from sensor toward object
        direction_x = x / distance
        direction_y = y / distance

        # Positive when object moves toward sensor
        closing_speed = -(
            velocity_x * direction_x +
            velocity_y * direction_y
        )

        return max(
            0.0,
            closing_speed
        )

    def calculate_time_to_collision(
        self,
        distance,
        closing_speed
    ):
        """
        Estimate time-to-collision in seconds.

        If the object is not approaching,
        TTC is infinite.
        """

        if closing_speed <= 0:
            return float("inf")

        return distance / closing_speed

    def calculate_risk_score(
        self,
        distance,
        closing_speed,
        ttc
    ):
        """
        Calculate a normalized dynamic risk score
        between 0 and 1.

        Higher risk means:
        - closer object
        - faster closing speed
        - shorter TTC
        """

        # Distance component
        distance_score = max(
            0.0,
            min(
                1.0,
                1.0 - (distance / 50.0)
            )
        )

        # Closing-speed component
        speed_score = max(
            0.0,
            min(
                1.0,
                closing_speed / 10.0
            )
        )

        # TTC component
        if math.isinf(ttc):
            ttc_score = 0.0
        else:
            ttc_score = max(
                0.0,
                min(
                    1.0,
                    1.0 - (ttc / 10.0)
                )
            )

        risk_score = (
            0.30 * distance_score +
            0.30 * speed_score +
            0.40 * ttc_score
        )

        return round(
            max(0.0, min(1.0, risk_score)),
            3
        )

    def calculate_risk(
        self,
        distance,
        velocity,
        position=None
    ):
        """
        Calculate dynamic risk level.

        Returns:
            HIGH
            MEDIUM
            LOW
        """

        if position is None:
            # Backward-compatible fallback.
            speed = self.calculate_speed(velocity)

            if speed == 0:
                closing_speed = 0.0
            else:
                closing_speed = speed
        else:
            closing_speed = self.calculate_closing_speed(
                position,
                velocity
            )

        ttc = self.calculate_time_to_collision(
            distance,
            closing_speed
        )

        risk_score = self.calculate_risk_score(
            distance,
            closing_speed,
            ttc
        )

        if (
            ttc <= 2.0
            or risk_score >= 0.75
        ):
            risk_level = "HIGH"

        elif (
            ttc <= 5.0
            or risk_score >= 0.45
        ):
            risk_level = "MEDIUM"

        else:
            risk_level = "LOW"

        return {
            "distance": round(distance, 3),
            "closing_speed": round(closing_speed, 3),
            "ttc": (
                float("inf")
                if math.isinf(ttc)
                else round(ttc, 3)
            ),
            "risk_score": risk_score,
            "risk_level": risk_level
        }