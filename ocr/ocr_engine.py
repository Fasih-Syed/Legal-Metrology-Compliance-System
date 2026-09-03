from paddleocr import PaddleOCR


ocr = PaddleOCR(
    lang="en",
    enable_mkldnn=False,
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)


def extract_text(image):
    """
    Extracts text from a preprocessed product image.
    """

    results = ocr.predict(image)

    extracted_text = []

    for result in results:
        print("\nOCR RESULT KEYS:")
    print(result.keys())
    
    if "rec_texts" in result:
            extracted_text.extend(result["rec_texts"])

    return extracted_text


def extract_text_with_boxes(image):
    """
    Extracts OCR text together with its bounding boxes.

    Returns a list containing:
    - detected text
    - bounding box coordinates
    """

    results = ocr.predict(image)

    extracted_data = []

    for result in results:

        texts = result.get("rec_texts", [])
        boxes = result.get("rec_boxes", [])

        for text, box in zip(texts, boxes):

            extracted_data.append({
                "text": text,
                "box": box.tolist() if hasattr(box, "tolist") else box
            })

    return extracted_data