import cv2

from qr_analysis.qr_scanner import scan_qr_code


IMAGE_PATH = "sample.jpeg"

image = cv2.imread(IMAGE_PATH)

result = scan_qr_code(image)


print("\n========== QR CODE ANALYSIS ==========\n")

print("Status:", result["status"])
print("QR Data:", result["data"])
print("Location:", result["points"])