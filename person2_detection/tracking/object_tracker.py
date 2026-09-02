import math


class ObjectTracker:
    """
    Lightweight 3D object tracker.

    Matches objects between frames using:
    1. Same class name
    2. Nearest spatial position
    """

    def __init__(self, max_match_distance=5.0):

        self.max_match_distance = max_match_distance

        self.previous_objects = {}

        self.next_track_id = 1


    def _calculate_distance(
        self,
        pos1,
        pos2
    ):

        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        dz = pos1[2] - pos2[2]

        return math.sqrt(
            dx ** 2 +
            dy ** 2 +
            dz ** 2
        )


    def update(self, detections):
        """
        Assign stable track IDs to detections.

        Parameters:
            detections: list of Detection objects

        Returns:
            detections with updated object_id
        """

        current_objects = {}

        used_previous_ids = set()

        for detection in detections:

            current_position = (
                detection.x,
                detection.y,
                detection.z
            )

            best_match_id = None

            best_distance = float("inf")

            # Search previous frame objects
            for track_id, previous_data in self.previous_objects.items():

                # Prevent one old object from matching
                # multiple current detections
                if track_id in used_previous_ids:
                    continue

                # Same class required
                if (
                    previous_data["class_name"]
                    != detection.class_name
                ):
                    continue

                previous_position = (
                    previous_data["position"]
                )

                distance = self._calculate_distance(
                    current_position,
                    previous_position
                )

                # Find closest valid match
                if (
                    distance < best_distance
                    and distance <= self.max_match_distance
                ):

                    best_distance = distance
                    best_match_id = track_id


            # Existing object found
            if best_match_id is not None:

                detection.object_id = best_match_id

                used_previous_ids.add(
                    best_match_id
                )

            # New object
            else:

                detection.object_id = (
                    f"track_{self.next_track_id}"
                )

                self.next_track_id += 1


            # Store object for next frame
            current_objects[
                detection.object_id
            ] = {
                "class_name":
                    detection.class_name,

                "position":
                    current_position
            }


        # Current frame becomes previous frame
        self.previous_objects = current_objects

        return detections