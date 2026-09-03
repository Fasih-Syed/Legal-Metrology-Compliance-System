from declaration.declaration_extractor import extract_declarations

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
    "For Customer Complaints/Feedback",
    "Customer Care Executive on:",
    "+91 8800344705",
    "wecare@moonstoneventures.in",
    "fsa Lic No. 133239990008",
    "MADE IN INDIA",
    "8906167241268"
]



result = extract_declarations(ocr_text)


for field, value in result.items():
    print(f"{field}: {value}")