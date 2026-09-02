from typing import Any, Dict, List

import pandas as pd

from person2_detection.detection.postprocess import postprocess_predictions
from tracking.pipeline import TrackingRiskPipeline
from adaptive.policy import apply_adaptive_resolution


class DRISHTIIntegrationPipeline:
    """
    Orchestrates the detection, tracking/risk, and adaptive-resolution
    components of the DRISHTI system.
    """

    def __init__(self, grid_size: float = 0.5):
        if grid_size <= 0:
            raise ValueError("grid_size must be greater than zero.")

        self.grid_size = grid_size
        self.tracking_pipeline = TrackingRiskPipeline()

    def process_detections(
        self,
        predictions: Dict[str, Any],
        frame_id: str = "unknown",
    ) -> List[Dict[str, Any]]:
        """Process detector predictions through detection and tracking."""

        detections = postprocess_predictions(
            predictions,
            frame_id=frame_id,
        )

        results = []

        for detection in detections:
            tracking_result = self.tracking_pipeline.process_detection(
                detection
            )

            results.append({
                "object_id": detection.object_id,
                "class_name": detection.class_name,
                "confidence": detection.confidence,
                "position": {
                    "x": detection.x,
                    "y": detection.y,
                    "z": detection.z,
                },
                "distance": {
                    "xy": detection.distance_xy,
                    "3d": detection.distance_3d,
                },
                "dimensions": {
                    "length": detection.length,
                    "width": detection.width,
                    "height": detection.height,
                },
                "heading": detection.heading,
                "frame_id": detection.frame_id,
                "timestamp": detection.timestamp,

                "motion": {
                    "vx": tracking_result["vx"],
                    "vy": tracking_result["vy"],
                    "speed": tracking_result["speed"],
                    "direction": tracking_result["direction"],
                },

                "trajectory": tracking_result["trajectory"],

                "risk": {
                    "closing_speed": tracking_result["closing_speed"],
                    "ttc": tracking_result["ttc"],
                    "risk_score": tracking_result["risk_score"],
                    "risk_level": tracking_result["risk_level"],
                },
            })

        return results

    def process_map(
        self,
        map_2_5d: pd.DataFrame,
    ) -> pd.DataFrame:
        """Apply adaptive resolution to a 2.5D map."""

        if not isinstance(map_2_5d, pd.DataFrame):
            raise TypeError("map_2_5d must be a pandas DataFrame")

        return apply_adaptive_resolution(map_2_5d)

    def get_object_resolution(
        self,
        x: float,
        y: float,
        adaptive_map: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Find the adaptive-resolution cell containing an object.

        The grid calculation matches lidar.projection.project_to_2_5d().
        """

        grid_x = int(x // self.grid_size)
        grid_y = int(y // self.grid_size)

        matching_cells = adaptive_map[
            (adaptive_map["grid_x"] == grid_x)
            & (adaptive_map["grid_y"] == grid_y)
        ]

        if matching_cells.empty:
            return {
                "resolution_level": "LOW",
                "resolution_m": 1.0,
                "grid_x": grid_x,
                "grid_y": grid_y,
            }

        cell = matching_cells.iloc[0]

        return {
            "resolution_level": str(cell["resolution_level"]),
            "resolution_m": float(cell["resolution_m"]),
            "grid_x": grid_x,
            "grid_y": grid_y,
        }

    def process_frame(
        self,
        predictions: Dict[str, Any],
        map_2_5d: pd.DataFrame,
        frame_id: str = "unknown",
    ) -> Dict[str, Any]:
        """
        Process one frame through detection, tracking/risk,
        and adaptive-resolution mapping.
        """

        detections = self.process_detections(
            predictions,
            frame_id=frame_id,
        )

        adaptive_map = self.process_map(
            map_2_5d
        )

        for detection in detections:
            resolution = self.get_object_resolution(
                x=detection["position"]["x"],
                y=detection["position"]["y"],
                adaptive_map=adaptive_map,
            )

            detection["risk_level"] = detection["risk"]["risk_level"]
            detection["recommended_resolution"] = (
                resolution["resolution_level"]
            )
            detection["resolution_m"] = resolution["resolution_m"]
            detection["adaptive_cell"] = {
                "grid_x": resolution["grid_x"],
                "grid_y": resolution["grid_y"],
            }

        return {
            "frame_id": frame_id,
            "detections": detections,
            "adaptive_map": adaptive_map,
        }
