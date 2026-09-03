import cv2

from visual_analysis.readability import calculate_image_quality


IMAGE_PATH = "sample.jpeg"


image = cv2.imread(IMAGE_PATH)

result = calculate_image_quality(image)


print("\n========== IMAGE QUALITY ==========\n")

print("Status:", result["status"])
print("Contrast:", result.get("contrast"))
print("Sharpness:", result.get("sharpness"))
print("Brightness:", result.get("brightness"))

print("\nWarnings:")

for warning in result.get("warnings", []):
    print("⚠", warning)