import pickle

import cv2 as cv
import numpy as np

from config import DEBUG, INPUT_VIDEO, OUTPUT_VIDEO, SPACE_THRESHOLD, SPACES_FILE


def load_spaces():
    try:
        with open(SPACES_FILE, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(
            "Error: 'spaces.pkl' not found. Run 'python setup_spaces.py' first to define the parking spaces."
        )
        exit(1)
    except (pickle.UnpicklingError, EOFError):
        print(
            "Error: 'spaces.pkl' is corrupted or invalid. Run 'python setup_spaces.py' again to generate a new one."
        )
        exit(1)


def process_frame(frame):
    gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    blurred_image = cv.GaussianBlur(gray_image, (5, 5), 0)

    # Binariza a imagem considerando a iluminação local.
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

        # Quantidade de pixels detectados na região da vaga.
        count = cv.countNonZero(space)

        if not DEBUG:
            cv.putText(
                frame,
                str(space_number),
                (x + 5, y + 20),
                cv.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )

        else:
            # Mostra o valor usado na calibração do SPACE_THRESHOLD.
            cv.putText(
                frame,
                str(count),
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

    if DEBUG:
        cv.putText(
            frame,
            f"THRESHOLD:{SPACE_THRESHOLD}",
            (700, 45),
            cv.FONT_HERSHEY_SIMPLEX,
            1.5,
            (255, 0, 0),
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

        if DEBUG:
            cv.imshow("Parking Vision resultado da função dilated_image", dilated_image)

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
