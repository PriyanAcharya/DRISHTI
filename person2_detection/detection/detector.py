class PointPillarsDetector:
    """
    Interface for PointPillars / OpenPCDet inference.

    Actual inference will run in a GPU environment.
    This class keeps the integration interface clean
    for the main Person 2 pipeline.
    """

    def __init__(
        self,
        config_path=None,
        checkpoint_path=None,
        confidence_threshold=0.30
    ):

        self.config_path = config_path

        self.checkpoint_path = checkpoint_path

        self.confidence_threshold = confidence_threshold

        self.model = None


    def load_model(self):
        """
        Load the PointPillars model.

        The GPU/OpenPCDet implementation will be
        connected here.
        """

        raise NotImplementedError(
            "PointPillars inference must be configured "
            "in the GPU environment."
        )


    def detect(
        self,
        points
    ):
        """
        Run object detection on a LiDAR point cloud.

        Input:
            NumPy array
            Shape: (N, 4)

            [x, y, z, intensity]

        Output:
            Raw detector predictions.
        """

        raise NotImplementedError(
            "GPU PointPillars inference not connected yet."
        )