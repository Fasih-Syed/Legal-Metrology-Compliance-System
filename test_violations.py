from declaration.declaration_extractor import extract_declarations
from compliance.rule_engine import check_required_declarations
from compliance.violation_detector import detect_violations


ocr_text = [
    "Premium Cumin Seeds Jeera Seeds",
    "Net Content : 100 g",
    "MRP:125.00",
    "USP:1.25/g",
    "BATCH NO : (RA) F081",
    "PACKED ON:29.06.2026",
    "USE BY :28.12.2026",
    "For the name, address, and FSSAI license number of",
    "the manufacturer or packer, scan the above QR code.",
    "Marketed By:",
    "Moonstone Ventures LLP",
    "M-33 (Basement), Lado Sarai,",
    "New Delhi South, Delhi -11030",
    "Customer Care Executive on:",
    "+91 8800344705",
    "wecare@moonstoneventures.in",
    "fsa Lic No. 133239990008",
    "MADE IN INDIA",
    "8906167241268"
]


# Step 1: Extract declarations
declarations = extract_declarations(ocr_text)

# Step 2: Run compliance checks
compliance_result = check_required_declarations(declarations)

# Step 3: Detect violations
result = detect_violations(compliance_result)


print("\n========== VIOLATION DETECTOR ==========\n")

print("Overall Status:")
print(result["overall_status"])

print("\nSummary:")
print(result["summary"])


print("\n========== PASSED ==========\n")

for item in result["passed"]:
    print(
        f"✓ {item['field']}: "
        f"{item['message']}"
    )


print("\n========== VIOLATIONS ==========\n")

for item in result["violations"]:
    print(
        f"✗ {item['field']}: "
        f"{item['message']}"
    )


print("\n========== REVIEW REQUIRED ==========\n")

for item in result["reviews"]:
    print(
        f"⚠ {item['field']}: "
        f"{item['message']}"
    )