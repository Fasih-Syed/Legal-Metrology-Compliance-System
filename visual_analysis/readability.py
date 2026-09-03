import cv2


def calculate_image_quality(image):
    """
    Calculates basic image-quality metrics that can
    affect OCR and declaration readability.
    """

    if image is None:
        return {
            "status": "ERROR",
            "message": "Image could not be loaded."
        }

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ---------------------------------------------------------
    # CONTRAST
    # ---------------------------------------------------------

    contrast = gray.std()

    # ---------------------------------------------------------
    # SHARPNESS
    # ---------------------------------------------------------

    sharpness = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    # ---------------------------------------------------------
    # BRIGHTNESS
    # ---------------------------------------------------------

    brightness = gray.mean()

    # ---------------------------------------------------------
    # BASIC QUALITY ASSESSMENT
    # ---------------------------------------------------------

    warnings = []

    if contrast < 25:
        warnings.append("Low image contrast.")

    if sharpness < 50:
        warnings.append("Image may be blurry.")

    if brightness < 40:
        warnings.append("Image may be too dark.")

    if brightness > 220:
        warnings.append("Image may be overexposed.")

    if warnings:
        status = "REVIEW_REQUIRED"
    else:
        status = "GOOD"

    return {
        "status": status,
        "contrast": round(float(contrast), 2),
        "sharpness": round(float(sharpness), 2),
        "brightness": round(float(brightness), 2),
        "warnings": warnings
    }