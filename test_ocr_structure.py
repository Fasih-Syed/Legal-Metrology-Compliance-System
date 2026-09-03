from image_processing.preprocessing import preprocess_image
from ocr.ocr_engine import extract_text_with_boxes


IMAGE_PATH = "sample.jpeg"


with open(IMAGE_PATH, "rb") as image_file:

    processed_image, _ = preprocess_image(image_file)


results = extract_text_with_boxes(processed_image)


print("\n========== OCR STRUCTURE ==========\n")

print("Total detected regions:", len(results))

for item in results:
    print("\nTEXT:", item["text"])
    print("BOX:", item["box"])