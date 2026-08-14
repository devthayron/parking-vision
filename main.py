import pickle

import cv2 as cv
import numpy as np

SPACE_THRESHOLD = 900


def load_spaces():
    with open("spaces.pkl", "rb") as file:
        return pickle.load(file)


def process_frame(frame):
    gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    blurred_image = cv.GaussianBlur(gray_image, (5, 5), 0)

    threshold_image = cv.adaptiveThreshold(
        blurred_image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16
    )

    median_image = cv.medianBlur(threshold_image, 5)

    kernel = np.ones((5, 5), np.uint8)
    dilated_image = cv.dilate(median_image, kernel=kernel)

    return dilated_image


def detect_spaces(frame, dilated_image, spaces):
    available_spaces = 0

    for space_number, (x, y, w, h) in enumerate(spaces, start=1):
        space = dilated_image[y : y + h, x : x + w]

        count = cv.countNonZero(space)

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

    return available_spaces


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
    video = cv.VideoCapture(input_video)

    if not video.isOpened():
        print("Error opening video.")
        return

    width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv.CAP_PROP_FPS)

    codec = cv.VideoWriter_fourcc(*"mp4v")

    output = cv.VideoWriter(output_video, codec, fps, (width, height))

    total_spaces = len(spaces)

    while True:
        success, frame = video.read()

        if not success:
            break

        dilated_image = process_frame(frame)

        available_spaces = detect_spaces(frame, dilated_image, spaces)

        draw_counter(frame, available_spaces, total_spaces)

        output.write(frame)

        cv.imshow("Parking Vision", frame)

        if cv.waitKey(10) & 0xFF == ord("q"):
            break

    video.release()
    output.release()
    cv.destroyAllWindows()

    print(f"Video generated: {output_video}")


def main():
    spaces = load_spaces()

    create_result_video("media/video.mp4", "media/video_result.mp4", spaces)


if __name__ == "__main__":
    main()
