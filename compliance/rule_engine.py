from typing import Dict, Any

from compliance.legal_requirements import LEGAL_REQUIREMENTS
from compliance.format_rules import validate_unit_sale_price


def check_required_declarations(
    declarations: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Compares extracted declarations against the configured
    legal requirements.

    This module performs first-level declaration validation.
    It does not make a final legal determination.
    """

    checks = {}

    for field, requirement in LEGAL_REQUIREMENTS.items():

        # Visual rules are handled separately.
        if requirement["check_type"] == "visual_analysis":
            checks[field] = {
                "status": "PENDING_VISUAL_ANALYSIS",
                "value": None,
                "message": (
                    "This requirement requires image-based "
                    "visual analysis."
                ),
                "requirement": requirement["name"],
                "source": requirement["source"]
            }

            continue

        value = declarations.get(field)

        # -----------------------------------------------------
        # MANUFACTURER / PACKER
        # -----------------------------------------------------

        if field == "manufacturer":

            if value:
                status = "FOUND"
                message = (
                    "Manufacturer / packer information detected."
                )

            elif declarations.get("manufacturer_source") == "QR code":
                status = "QR_REFERENCED"
                message = (
                    "Manufacturer / packer information is "
                    "referenced through a QR code."
                )

            else:
                status = "NOT_FOUND"
                message = (
                    "Manufacturer / packer information "
                    "was not detected."
                )

        # -----------------------------------------------------
        # NORMAL PRESENCE CHECK
        # -----------------------------------------------------

        elif value:
            status = "FOUND"
            message = f"{requirement['name']} detected."

        else:
            status = "NOT_FOUND"
            message = (
                f"{requirement['name']} was not detected."
            )

        checks[field] = {
            "status": status,
            "value": value,
            "message": message,
            "requirement": requirement["name"],
            "source": requirement["source"]
        }

    # ---------------------------------------------------------
    # UNIT SALE PRICE VALIDATION
    # ---------------------------------------------------------

    unit_price_result = validate_unit_sale_price(
        net_quantity=declarations.get("net_quantity"),
        mrp=declarations.get("mrp"),
        declared_unit_price=declarations.get("unit_sale_price")
    )

    checks["unit_sale_price"] = {
        "status": unit_price_result["status"],
        "value": unit_price_result["declared"],
        "expected": unit_price_result["expected"],
        "message": unit_price_result["message"],
        "requirement": LEGAL_REQUIREMENTS["unit_sale_price"]["name"],
        "source": LEGAL_REQUIREMENTS["unit_sale_price"]["source"]
    }

    
    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    found_count = sum(
        1
        for check in checks.values()
        if check["status"] == "FOUND"
    )

    not_found_count = sum(
        1
        for check in checks.values()
        if check["status"] == "NOT_FOUND"
    )

    qr_referenced_count = sum(
        1
        for check in checks.values()
        if check["status"] == "QR_REFERENCED"
    )

    pending_visual_count = sum(
        1
        for check in checks.values()
        if check["status"] == "PENDING_VISUAL_ANALYSIS"
    )

    # ---------------------------------------------------------
    # OVERALL STATUS
    # ---------------------------------------------------------

    if not_found_count > 0:
        overall_status = "POTENTIAL_NON_COMPLIANCE"

    elif pending_visual_count > 0:
        overall_status = "REVIEW_REQUIRED"

    else:
        overall_status = "DECLARATIONS_DETECTED"

    return {
        "overall_status": overall_status,

        "summary": {
            "found": found_count,
            "not_found": not_found_count,
            "qr_referenced": qr_referenced_count,
            "pending_visual_analysis": pending_visual_count
        },

        "checks": checks
    }