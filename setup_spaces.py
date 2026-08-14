import pickle

import cv2 as cv


def select_spaces(img, quantity):
    spaces = []

    for number in range(1, quantity + 1):
        space = cv.selectROI(f"Select parking space {number}", img, False)

        cv.destroyWindow(f"Select parking space {number}")

        spaces.append(space)

        cv.rectangle(
            img,
            (space[0], space[1]),
            (space[0] + space[2], space[1] + space[3]),
            (255, 0, 0),
            2,
        )

        cv.putText(
            img,
            str(number),
            (space[0] + 5, space[1] + 20),
            cv.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

    return spaces


def save_spaces(spaces):
    with open("spaces.pkl", "wb") as file:
        pickle.dump(spaces, file)


def main():
    img = cv.imread("media/parking.png")

    spaces = select_spaces(img, 69)

    save_spaces(spaces)


if __name__ == "__main__":
    main()
