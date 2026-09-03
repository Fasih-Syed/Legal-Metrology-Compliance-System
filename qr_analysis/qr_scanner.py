import cv2


def _found_result(data, points):
    """Build result for a successfully decoded QR code."""
    return {
        "status": "FOUND",
        "data": data,
        "points": points.tolist() if points is not None else None,
    }


def _detected_result(points):
    """Build result when QR is detected but cannot be decoded."""
    return {
        "status": "DETECTED_NOT_READABLE",
        "data": None,
        "points": points.tolist() if points is not None else None,
    }


def _decode_multi(detector, image):
    """Try detecting and decoding multiple QR codes."""

    try:
        retval, decoded_info, points, _ = (
            detector.detectAndDecodeMulti(image)
        )
    except Exception:
        return None

    if not retval or points is None:
        return None

    # QR detected but nothing could be decoded
    if not decoded_info:
        return _detected_result(points)

    for data in decoded_info:

        if data:
            return _found_result(data, points)

    # QR points exist, but all decoded strings are empty
    return _detected_result(points)


def _decode_single(detector, image):
    """Try detecting and decoding a single QR code."""

    try:
        data, points, _ = detector.detectAndDecode(image)
    except Exception:
        return None

    if data:
        return _found_result(data, points)

    # OpenCV detected a QR but couldn't decode it
    if points is not None:
        return _detected_result(points)

    return None


def _try_image(detector, image):
    """Try several decoding methods on one image."""

    # 1. Multi-code detection
    result = _decode_multi(detector, image)

    if result:
        if result["status"] == "FOUND":
            return result

        detected_result = result
    else:
        detected_result = None

    # 2. Single-code detection
    result = _decode_single(detector, image)

    if result:
        if result["status"] == "FOUND":
            return result

        if detected_result is None:
            detected_result = result

    return detected_result


def _first_scan_result(detector, images):
    """Return the first successful result, retaining any detection."""
    detected_result = None

    for image in images:
        result = _try_image(detector, image)
        if not result:
            continue
        if result["status"] == "FOUND":
            return result
        if detected_result is None:
            detected_result = result

    return detected_result


def _not_found_result():
    """Build a result when no QR code was found."""
    return {
        "status": "NOT_FOUND",
        "data": None,
        "points": None
    }


def scan_qr_code(image):
    """
    Detects and decodes QR codes from a product image.

    Status values:
        FOUND
        DETECTED_NOT_READABLE
        NOT_FOUND
    """

    detector = cv2.QRCodeDetector()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    enlarged = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )
    _, threshold = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    result = _first_scan_result(detector, (image, gray, enlarged, threshold))
    return result if result else _not_found_result()