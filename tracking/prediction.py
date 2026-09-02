def predict_position(obj, prediction_time):
    """
    Predict future 3D position using constant velocity.

    Expected obj fields:
        x, y, z, vx, vy
    """
    return {
        "x": obj["x"] + obj["vx"] * prediction_time,
        "y": obj["y"] + obj["vy"] * prediction_time,
        "z": obj.get("z", 0.0),
        "time": prediction_time
    }


def predict_trajectory(obj, horizon=3.0, step=0.25):
    """
    Generate future trajectory points.

    horizon:
        Prediction duration in seconds.

    step:
        Time interval between prediction points.
    """
    if horizon < 0:
        raise ValueError("horizon must be >= 0")

    if step <= 0:
        raise ValueError("step must be > 0")

    trajectory = []

    t = 0.0

    while t <= horizon + 1e-9:
        trajectory.append(
            predict_position(obj, t)
        )
        t += step

    return trajectory