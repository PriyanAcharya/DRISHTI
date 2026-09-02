class ObjectTracker:
    """
    Tracks objects across consecutive frames
    and stores their position history.
    """

    def __init__(self, history_size=10):
        self.objects = {}
        self.next_id = 1
        self.history_size = history_size

    def update(self, detections):
        """
        Update tracked objects using the latest detections.

        Each detection should contain:
            - label
            - position

        Returns:
            list: Tracked objects with IDs and position history.
        """

        tracked_objects = []

        for detection in detections:

            matched_id = None

            # Try to match the detection with an existing object
            for object_id, previous_object in self.objects.items():

                if previous_object["label"] == detection["label"]:
                    matched_id = object_id
                    break

            # Create a new ID if no matching object exists
            if matched_id is None:
                matched_id = self.next_id
                self.next_id += 1

                position_history = [
                    detection["position"]
                ]

            else:
                position_history = self.objects[
                    matched_id
                ]["position_history"].copy()

                position_history.append(
                    detection["position"]
                )

                # Keep only the latest positions
                if len(position_history) > self.history_size:
                    position_history.pop(0)

            tracked_object = {
                "id": matched_id,
                "label": detection["label"],
                "position": detection["position"],
                "position_history": position_history.copy()
            }

            self.objects[matched_id] = tracked_object
            tracked_objects.append(
                tracked_object.copy()
            )

        return tracked_objects


# Simple test
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