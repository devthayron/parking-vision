import pickle

import cv2 as cv

from config import PARKING_IMAGE, SPACES_FILE


def select_spaces(img):
    spaces = []
    number = 1

    while True:
        window_name = f"Select parking space {number}"

        space = cv.selectROI(window_name, img, False)

        cv.destroyWindow(window_name)

        # Tecla 'c' cancela e encerra a seleção.
        if space[2] == 0 or space[3] == 0:
            break

        x, y, w, h = space

        spaces.append(
            {
                "id": number,
                "bbox": (x, y, w, h),
            }
        )

        cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv.putText(
            img,
            str(number),
            (x + 5, y + 20),
            cv.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        number += 1

    return spaces


def save_spaces(spaces):
    with open(SPACES_FILE, "wb") as file:
        pickle.dump(spaces, file)


def main():
    img = cv.imread(PARKING_IMAGE)

    spaces = select_spaces(img)

    print(f"{len(spaces)} vagas selecionadas.")

    if spaces:
        save_spaces(spaces)
        print(f"Vagas salvas em: {SPACES_FILE}")
    else:
        print("Nenhuma vaga foi salva.")


if __name__ == "__main__":
    main()
