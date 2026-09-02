from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Detection:
    """
    Standardized representation of one 3D LiDAR object detection.

    This is the output contract of Person 2's module and will be
    consumed by the adaptive-resolution module.
    """

    object_id: Optional[int]

    class_name: str
    confidence: float

    # 3D object center position (meters)
    x: float
    y: float
    z: float

    # 3D bounding box dimensions (meters)
    length: float
    width: float
    height: float

    # Object orientation in radians
    heading: float

    # Distance from LiDAR sensor
    distance_xy: float
    distance_3d: float
    
    importance_score: float = 0.0
    risk_level: str = "LOW"
    recommended_resolution: str = "LOW"
    motion_score: float = 0.0
    # Frame information
    frame_id: str = "" 
    timestamp: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert the detection into a JSON-ready dictionary."""

        return {
            "object_id": self.object_id,
            "class_name": self.class_name,
            "confidence": round(float(self.confidence), 4),

            "position": {
                "x": round(float(self.x), 4),
                "y": round(float(self.y), 4),
                "z": round(float(self.z), 4)
            },

            "dimensions": {
                "length": round(float(self.length), 4),
                "width": round(float(self.width), 4),
                "height": round(float(self.height), 4)
            },

            "heading": round(float(self.heading), 4),

            "distance": {
                "xy": round(float(self.distance_xy), 4),
                "3d": round(float(self.distance_3d), 4)
            },

            "frame_id": self.frame_id,
            "timestamp": self.timestamp
        }
    