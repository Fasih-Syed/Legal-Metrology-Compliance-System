import cv2
import numpy as np


def preprocess_image(uploaded_file):
    """
    Converts an uploaded image into a format suitable for OCR.
    """

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Unable to read the uploaded image.")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Improve contrast
    enhanced = cv2.equalizeHist(gray)

    return image, enhanced  