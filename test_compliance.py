from declaration.declaration_extractor import extract_declarations
from compliance.rule_engine import check_required_declarations


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


declarations = extract_declarations(ocr_text)

compliance_result = check_required_declarations(declarations)


print("\n========== DECLARATIONS ==========\n")

for field, value in declarations.items():
    print(f"{field}: {value}")


print("\n========== COMPLIANCE ==========\n")

print("Overall Status:")
print(compliance_result["overall_status"])

print("\nSummary:")
print(compliance_result["summary"])

print("\nChecks:")

for field, result in compliance_result["checks"].items():
    print(
        f"{field}: "
        f"{result['status']} - "
        f"{result['message']}"
    )