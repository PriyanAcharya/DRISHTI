import math


class ObjectTracker:
    """
    Tracks objects across consecutive frames
    and stores their position history.

    Matching is based on:
    - Object label
    - Position distance

    This allows multiple objects of the same class
    to be tracked separately.
    """

    def __init__(
        self,
        history_size=10,
        max_match_distance=5.0
    ):
        self.objects = {}
        self.next_id = 1
        self.history_size = history_size
        self.max_match_distance = max_match_distance

    def _distance(self, position_a, position_b):
        """
        Calculate Euclidean distance between two 2D positions.
        """
        dx = position_a[0] - position_b[0]
        dy = position_a[1] - position_b[1]

        return math.sqrt(
            dx ** 2 + dy ** 2
        )

    def update(self, detections):
        """
        Update tracked objects using the latest detections.

        Each detection should contain:
            - label
            - position

        Optional:
            - cell_id

        Returns:
            list: Tracked objects with IDs and position history.
        """

        tracked_objects = []

        # Keep track of IDs that have already been matched
        # during this frame.
        used_ids = set()

        for detection in detections:

            best_id = None
            best_distance = None

            # Find the nearest existing object with
            # the same label.
            for object_id, previous_object in self.objects.items():

                # Do not assign one old object to
                # multiple detections in the same frame.
                if object_id in used_ids:
                    continue

                if previous_object["label"] != detection["label"]:
                    continue

                distance = self._distance(
                    previous_object["position"],
                    detection["position"]
                )

                # Ignore objects that moved too far away.
                if distance > self.max_match_distance:
                    continue

                if (
                    best_distance is None
                    or distance < best_distance
                ):
                    best_id = object_id
                    best_distance = distance

            # No suitable previous object found.
            if best_id is None:

                matched_id = self.next_id
                self.next_id += 1

                position_history = [
                    detection["position"]
                ]

            else:

                matched_id = best_id

                position_history = self.objects[
                    matched_id
                ]["position_history"].copy()

                position_history.append(
                    detection["position"]
                )

                # Keep only the latest positions.
                if len(position_history) > self.history_size:
                    position_history.pop(0)

                used_ids.add(matched_id)

            tracked_object = {
                "id": matched_id,
                "label": detection["label"],
                "position": detection["position"],
                "position_history": position_history.copy(),

                # Optional spatial information.
                # Keeps working even if older detections
                # don't contain cell_id.
                "cell_id": detection.get("cell_id")
            }

            self.objects[matched_id] = tracked_object

            tracked_objects.append(
                tracked_object.copy()
            )

        return tracked_objects


# Simple manual test
if __name__ == "__main__":

    tracker = ObjectTracker()

    frame1 = [
        {
            "label": "person",
            "position": (10, 5)
        }
    ]

    frame2 = [
        {
            "label": "person",
            "position": (13, 7)
        }
    ]

    frame3 = [
        {
            "label": "person",
            "position": (16, 9)
        }
    ]

    print("Frame 1:")
    print(tracker.update(frame1))

    print("\nFrame 2:")
    print(tracker.update(frame2))

    print("\nFrame 3:")
    print(tracker.update(frame3))