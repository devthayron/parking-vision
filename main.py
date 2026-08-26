import pickle
import sys

import cv2 as cv

from config import DEBUG, INPUT_VIDEO, OUTPUT_VIDEO, SPACES_FILE
from detector import create_detector


def load_spaces():
    try:
        with open(SPACES_FILE, "rb") as file:
            return pickle.load(file)

    except FileNotFoundError:
        print(
            "Error: 'spaces.pkl' not found. "
            "Run 'python setup_spaces.py' first to define the parking spaces."
        )
        sys.exit(1)

    except (pickle.UnpicklingError, EOFError):
        print(
            "Error: 'spaces.pkl' is corrupted or invalid. "
            "Run 'python setup_spaces.py' again to generate a new one."
        )
        sys.exit(1)


def draw_counter(frame, available_spaces, total_spaces):
    cv.rectangle(frame, (37, 5), (370, 60), (0, 255, 0), -1)

    cv.putText(
        frame,
        f"LIVRES: {available_spaces}/{total_spaces}",
        (50, 45),
        cv.FONT_HERSHEY_SIMPLEX,
        1.5,
        (255, 255, 255),
        5,
    )


def create_result_video(input_video, output_video, spaces):
    """
    Processes the input video, detects parking space occupancy,
    and generates a result video.
    """
    video = cv.VideoCapture(input_video)

    if not video.isOpened():
        print("Error opening video.")
        return

    width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv.CAP_PROP_FPS)

    codec = cv.VideoWriter_fourcc(*"mp4v")
    output = cv.VideoWriter(output_video, codec, fps, (width, height))

    detector = create_detector()
    total_spaces = len(spaces)

    while True:
        success, frame = video.read()

        if not success:
            break

        available_spaces, processed_frame = detector.detect(frame, spaces)

        draw_counter(frame, available_spaces, total_spaces)

        output.write(frame)

        cv.imshow("Parking Vision", frame)

        if DEBUG:
            cv.imshow(
                "Parking Vision - Processed Image",
                processed_frame,
            )

        if cv.waitKey(30) & 0xFF == ord("q"):
            break

    video.release()
    output.release()
    cv.destroyAllWindows()

    print(f"Video generated: {output_video}")


def main():
    spaces = load_spaces()

    create_result_video(INPUT_VIDEO, OUTPUT_VIDEO, spaces)


if __name__ == "__main__":
    main()
