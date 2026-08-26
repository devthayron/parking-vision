import cv2 as cv
import numpy as np

from config import DEBUG, DETECTION_METHOD, SPACE_THRESHOLD


class OccupancyDetector:
    """
    Detects parking space occupancy based on the number
    of detected pixels within each parking space.
    """

    def process_frame(self, frame):
        """
        Applies image processing techniques to prepare the frame
        for parking space occupancy analysis.
        """
        gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        blurred_image = cv.GaussianBlur(gray_image, (5, 5), 0)

        threshold_image = cv.adaptiveThreshold(
            blurred_image,
            255,
            cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv.THRESH_BINARY_INV,
            51,
            16,
        )

        median_image = cv.medianBlur(threshold_image, 5)

        kernel = np.ones((5, 5), np.uint8)
        dilated_image = cv.dilate(median_image, kernel=kernel)

        return dilated_image

    def detect(self, frame, spaces):
        """
        Analyzes each parking space and classifies it as available
        or occupied based on the number of detected pixels.

        Returns the number of available spaces and the processed frame.
        """
        processed_frame = self.process_frame(frame)

        available_spaces = 0

        for space in spaces:
            space_number = space["id"]
            x, y, w, h = space["bbox"]

            space_image = processed_frame[y : y + h, x : x + w]

            count = cv.countNonZero(space_image)

            if DEBUG:
                cv.putText(
                    frame,
                    str(count),
                    (x + 5, y + 20),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2,
                )
            else:
                cv.putText(
                    frame,
                    str(space_number),
                    (x + 5, y + 20),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2,
                )

            if count <= SPACE_THRESHOLD:
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                available_spaces += 1

            else:
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        return available_spaces, processed_frame


def create_detector():
    if DETECTION_METHOD == "pixel":
        return OccupancyDetector()

    raise ValueError(f"Unknown detection method: {DETECTION_METHOD}")
