import cv2
import numpy as np


def decode_image(data):
    array = np.frombuffer(data, dtype=np.uint8).copy()
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Invalid image")

    return image


def resize_image(image, max_width=800, max_height=600):
    height, width = image.shape[:2]

    if width == max_width and height == max_height:
        return image

    return cv2.resize(image, (max_width, max_height))


def to_grayscale(image):
    if image.ndim == 2:
        return image

    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def preprocess_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    saturation = hsv[:, :, 1]

    _, binary = cv2.threshold(
        saturation,
        60,
        255,
        cv2.THRESH_BINARY_INV
    )

    return binary