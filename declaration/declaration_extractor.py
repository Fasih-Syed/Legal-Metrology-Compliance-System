import re


def normalize_text(text_lines):
    """
    Combines OCR lines into one searchable text block.
    """

    text = " ".join(text_lines)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_declarations(text_lines):
    """
    Extracts structured product declarations from OCR output.
    """

    text = normalize_text(text_lines)

    declarations = {
        "product_name": None,
        "net_quantity": None,
        "mrp": None,
        "unit_sale_price": None,
        "batch_number": None,
        "packed_on": None,
        "use_by": None,
        "manufacturer": None,
        "marketed_by": None,
        "address": None,
        "customer_care": None,
        "email": None,
        "fssai_license": None,
        "barcode": None,
        "country_of_origin": None,
        "manufacturer_source": None
    }

    # ---------------------------------------------------------
    # PRODUCT NAME
    # ---------------------------------------------------------

    product_match = re.search(
        r"(premium\s+cumin\s+seeds(?:\s*/?\s*jeera\s+seeds)?)",
        text,
        re.IGNORECASE
    )

    if product_match:
        declarations["product_name"] = product_match.group(1).strip()

    # ---------------------------------------------------------
    # NET QUANTITY
    # ---------------------------------------------------------

    quantity_match = re.search(
        r"(?:net\s+(?:content|quantity|wt|weight))"
        r"\s*[:\-]?\s*"
        r"([\d.]+\s*(?:mg|g|kg|ml|l))",
        text,
        re.IGNORECASE
    )

    if quantity_match:
        declarations["net_quantity"] = quantity_match.group(1).strip()

    # ---------------------------------------------------------
    # MRP
    # ---------------------------------------------------------

    mrp_match = re.search(
        r"\bMRP\s*[:\-]?\s*"
        r"(?:₹|Rs\.?|INR)?\s*"
        r"([\d,]+(?:\.\d{1,2})?)",
        text,
        re.IGNORECASE
    )

    if mrp_match:
        declarations["mrp"] = mrp_match.group(1)

            # ---------------------------------------------------------
    # UNIT SALE PRICE
    # Examples:
    # USP: 1.25/g
    # Rs. 1.25 per g
    # ₹1.25/g
    # ---------------------------------------------------------

    unit_price_match = re.search(
        r"(?:USP|unit\s+sale\s+price)"
        r"\s*[:\-]?\s*"
        r"(?:₹|Rs\.?|INR)?\s*"
        r"([\d,]+(?:\.\d{1,2})?)"
        r"\s*(?:/|per)\s*"
        r"(g|kg|mg|ml|l|cm|m|number|unit)",
        text,
        re.IGNORECASE
    )

    if unit_price_match:
        declarations["unit_sale_price"] = {
            "price": unit_price_match.group(1),
            "unit": unit_price_match.group(2).lower()
        }

    # ---------------------------------------------------------
    # BATCH NUMBER
    # ---------------------------------------------------------
    # ---------------------------------------------------------
    # BATCH NUMBER
    # ---------------------------------------------------------

    batch_match = re.search(
        r"(?:batch\s*(?:no|number)?|lot\s*(?:no|number)?)"
        r"\s*[:\-]?\s*"
        r"([A-Z0-9()\/-]+(?:\s+[A-Z0-9()\/-]+)?)"
        r"(?=\s+(?:packed|packed\s+on|use\s+by|expiry)|$)",
        text,
        re.IGNORECASE
    )

    if batch_match:
        declarations["batch_number"] = batch_match.group(1).strip()
    # ---------------------------------------------------------
    # PACKED ON
    # ---------------------------------------------------------

    packed_match = re.search(
        r"(?:packed\s*on|packed)"
        r"\s*[:\-]?\s*"
        r"(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})",
        text,
        re.IGNORECASE
    )

    if packed_match:
        declarations["packed_on"] = packed_match.group(1)

    # ---------------------------------------------------------
    # USE BY / EXPIRY
    # ---------------------------------------------------------

    expiry_match = re.search(
        r"(?:use\s*by|best\s*before|expiry)"
        r"\s*[:\-]?\s*"
        r"(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})",
        text,
        re.IGNORECASE
    )

    if expiry_match:
        declarations["use_by"] = expiry_match.group(1)

    # ---------------------------------------------------------
    # ---------------------------------------------------------
    # MARKETED BY
# ---------------------------------------------------------

    marketed_match = re.search(
    r"marketed\s+by\s*:\s*"
    r"([A-Za-z][A-Za-z0-9&.,'()\- ]{2,80}?)"
    r"(?=\s+(?:M[-\s]?\d|for\s+customer|customer\s+care|fsa|fssai|storage|made\s+in|refer|and\s+map)|$)",
        text,
        re.IGNORECASE
    )

    if marketed_match:
        declarations["marketed_by"] = marketed_match.group(1).strip()


# ---------------------------------------------------------
    # ADDRESS
# ---------------------------------------------------------

    address_match = re.search(
    r"(M[-\s]?\d+"
    r"\s*\([^)]*\)"
    r".*?"
    r"(?:Delhi|Hyderabad|Mumbai|Bangalore|Bengaluru)"
    r"\s*[-–]?\s*\d{5,6})",
        text,
        re.IGNORECASE
    )

    if address_match:
        declarations["address"] = address_match.group(1).strip()
    
    # ---------------------------------------------------------
    # CUSTOMER CARE
    # ---------------------------------------------------------

    phone_match = re.search(
        r"(?:customer\s*care|call|contact)"
        r".*?"
        r"(\+91[\s-]?\d{10}|\d{10})",
        text,
        re.IGNORECASE
    )

    if phone_match:
        declarations["customer_care"] = phone_match.group(1)

    # ---------------------------------------------------------
    # EMAIL
    # ---------------------------------------------------------

    email_match = re.search(
        r"[\w\.-]+@[\w\.-]+\.\w+",
        text
    )

    if email_match:
        declarations["email"] = email_match.group(0)

    # ---------------------------------------------------------
    # FSSAI LICENSE
    # Handles:
    # FSSAI Lic No.
    # FSA Lic No.
    # FSSAI License No.
    # FSAI Lic No.
    # ---------------------------------------------------------

    fssai_match = re.search(
        r"(?:fssai|fsa|fsai)"
        r"\s*"
        r"(?:lic|license|licence)"
        r"\s*"
        r"(?:no|number)?"
        r"\.?\s*[:\-]?\s*"
        r"(\d{10,15})",
        text,
        re.IGNORECASE
    )

    if fssai_match:
        declarations["fssai_license"] = fssai_match.group(1)

    # ---------------------------------------------------------
    # BARCODE
    # ---------------------------------------------------------

    barcode_matches = re.findall(
        r"\b\d{13}\b",
        text
    )

    if barcode_matches:
        declarations["barcode"] = barcode_matches[0]

    # ---------------------------------------------------------
    # COUNTRY OF ORIGIN
    # ---------------------------------------------------------

    country_match = re.search(
        r"made\s+in\s+([A-Za-z ]+?)(?=\s|$)",
        text,
        re.IGNORECASE
    )

    if country_match:
        declarations["country_of_origin"] = country_match.group(1).strip()

    # ---------------------------------------------------------
    # MANUFACTURER / PACKER SOURCE
    # ---------------------------------------------------------

    qr_match = re.search(
        r"(?:manufacturer|packer)"
        r".{0,200}?"
        r"(?:scan|QR|code)",
        text,
        re.IGNORECASE
    )

    if qr_match:
        declarations["manufacturer_source"] = "QR code"

    return declarations