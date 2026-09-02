from person2_detection.detection.postprocess import (
    postprocess_predictions
)

from person2_detection.tracking.object_tracker import (
    ObjectTracker
)

from person2_detection.tracking.motion_estimator import (
    MotionEstimator
)

from person2_detection.scoring.importance import (
    score_detection
)


class AdaptiveDetectionPipeline:
    """
    Complete adaptive detection pipeline.

    Pipeline:

    Raw Predictions
        ↓
    Postprocessing
        ↓
    Object Tracking
        ↓
    Motion Estimation
        ↓
    Adaptive Importance Scoring
        ↓
    Risk Assessment
        ↓
    Resolution Recommendation
    """

    def __init__(self):

        self.tracker = ObjectTracker(
            max_match_distance=5.0
        )

        self.motion_estimator = MotionEstimator()


    def process_frame(
        self,
        predictions,
        frame_id
    ):

        # ---------------------------------
        # STEP 1: Convert raw predictions
        # into Detection objects
        # ---------------------------------

        detections = postprocess_predictions(
            predictions,
            frame_id=frame_id
        )


        # ---------------------------------
        # STEP 2: Assign stable tracking IDs
        # ---------------------------------

        detections = self.tracker.update(
            detections
        )


        # ---------------------------------
        # STEP 3: Calculate object motion
        # ---------------------------------

        for detection in detections:

            motion_score = (
                self.motion_estimator.calculate_motion(
                    object_id=detection.object_id,
                    x=detection.x,
                    y=detection.y,
                    z=detection.z
                )
            )
            detection.motion_score = motion_score

            # ---------------------------------
            # STEP 4: Recalculate adaptive score
            # with real motion information
            # ---------------------------------

            scoring_result = score_detection(
                class_name=detection.class_name,
                distance=detection.distance_xy,
                confidence=detection.confidence,
                motion_score=motion_score
            )


            # ---------------------------------
            # STEP 5: Update detection
            # ---------------------------------

            detection.importance_score = (
                scoring_result[
                    "importance_score"
                ]
            )

            detection.risk_level = (
                scoring_result[
                    "risk_level"
                ]
            )

            detection.recommended_resolution = (
                scoring_result[
                    "recommended_resolution"
                ]
            )


        return detections