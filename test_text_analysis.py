import cv2

from visual_analysis.textanalysis import analyze_text_regions


IMAGE_PATH = "sample.jpeg"

image = cv2.imread(IMAGE_PATH)

result = analyze_text_regions(image)

print("\n========== TEXT ANALYSIS ==========\n")

print("Status:", result["status"])
print("Image width:", result.get("image_width"))
print("Image height:", result.get("image_height"))
print("Text-like regions:", result.get("region_count"))

print("\nFirst 20 regions:")

for region in result.get("regions", [])[:20]:
    print(region)