def analyze_ocr_text_regions(ocr_data):
    """
    Analyzes bounding boxes returned by PaddleOCR.

    Estimates the size of each detected text region
    using its bounding-box dimensions.
    """

    if not ocr_data:
        return {
            "status": "NO_TEXT",
            "region_count": 0,
            "regions": []
        }

    regions = []

    for item in ocr_data:

        text = item.get("text", "")
        box = item.get("box")

        if not box or len(box) != 4:
            continue

        x1, y1, x2, y2 = box

        width = abs(x2 - x1)
        height = abs(y2 - y1)

        regions.append({
            "text": text,
            "x1": int(x1),
            "y1": int(y1),
            "x2": int(x2),
            "y2": int(y2),
            "width": int(width),
            "height": int(height)
        })

    return {
        "status": "SUCCESS",
        "region_count": len(regions),
        "regions": regions
    }