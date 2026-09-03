import cv2

from ocr.ocr_engine import extract_text_with_boxes
from visual_analysis.textanalysis import analyze_ocr_text_regions


IMAGE_PATH = "sample.jpeg"


image = cv2.imread(IMAGE_PATH)

ocr_data = extract_text_with_boxes(image)

result = analyze_ocr_text_regions(ocr_data)


print("\n========== OCR TEXT REGIONS ==========\n")

print("Status:", result["status"])
print("Detected text regions:", result["region_count"])

print("\nDetected regions:\n")

for region in result["regions"]:
    print(
        f"{region['text']} "
        f"| width={region['width']} "
        f"| height={region['height']}"
    )