
import os
import re

import cv2
import pytesseract


def configure_tesseract():
    command = os.environ.get("TESSERACT_CMD")

    if command:
        pytesseract.pytesseract.tesseract_cmd = command
        return

    default = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    if os.path.exists(default):
        pytesseract.pytesseract.tesseract_cmd = default


def tesseract_config():
    return "--oem 3 --psm 11"


def prepare_for_ocr(original, preprocessed=None):
    if original.ndim == 3:
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    else:
        gray = original.copy()

    height, width = gray.shape[:2]
    scale = max(2, min(4, 1800 // max(height, width)))

    enlarged = cv2.resize(
        gray,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC,
    )

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8),
    )
    enhanced = clahe.apply(enlarged)

    _, binary = cv2.threshold(
        enhanced,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    _, inverted = cv2.threshold(
        enhanced,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )

    adaptive = cv2.adaptiveThreshold(
        enhanced,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )

    candidates = [enlarged, enhanced, binary, inverted, adaptive]

    if preprocessed is not None:
        if preprocessed.ndim == 3:
            preprocessed = cv2.cvtColor(
                preprocessed,
                cv2.COLOR_BGR2GRAY,
            )
        candidates.append(preprocessed)

    return candidates


def _recognize_with_confidence(image, config):
    data = pytesseract.image_to_data(
        image,
        lang="eng",
        config=config,
        output_type=pytesseract.Output.DICT,
    )

    words = []
    confidences = []

    for word, confidence in zip(data["text"], data["conf"]):
        word = word.strip()

        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            continue

        if not word or confidence < 0:
            continue

        if not re.search(r"[A-Za-z0-9]", word):
            continue

        words.append(word)
        confidences.append(confidence)

    text = " ".join(words).strip()

    if not confidences:
        return text, 0.0

    average_confidence = sum(confidences) / len(confidences)
    useful_chars = len(re.findall(r"[A-Za-z0-9]", text))

    if useful_chars == 0:
        return "", 0.0

    score = average_confidence + min(useful_chars, 100) * 0.1

    return text, score


def extract_text(images, config=None):
    configure_tesseract()

    if not isinstance(images, (list, tuple)):
        images = [images]

    configs = [
        "--oem 3 --psm 11",
        "--oem 3 --psm 6",
        "--oem 3 --psm 3",
        "--oem 3 --psm 7",
        "--oem 3 --psm 8",
        "--oem 3 --psm 13",
    ]

    best_text = ""
    best_score = -1.0

    for image_index, image in enumerate(images, start=1):
        for ocr_config in configs:
            try:
                text, score = _recognize_with_confidence(
                    image,
                    ocr_config,
                )

                print(
                    f"OCR image={image_index}, "
                    f"config={ocr_config}, "
                    f"score={score:.2f}, "
                    f"text={text[:150]!r}"
                )

                if text and score > best_score:
                    best_text = text
                    best_score = score

            except pytesseract.TesseractError as error:
                print("Tesseract error:", error)

    print("Selected OCR result:", repr(best_text))
    return best_text

