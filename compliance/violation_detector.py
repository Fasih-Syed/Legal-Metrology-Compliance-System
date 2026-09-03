def detect_violations(compliance_result):
    """
    Converts compliance-engine checks into
    structured findings for reporting and UI.
    """

    violations = []
    warnings = []
    passed = []
    reviews = []

    checks = compliance_result.get("checks", {})

    for field, check in checks.items():

        status = check.get("status")
        requirement = check.get("requirement", field)
        message = check.get("message", "")
        value = check.get("value")

        # -----------------------------------------------------
        # PASSED
        # -----------------------------------------------------

        if status in ["FOUND", "VALID"]:
            passed.append({
                "field": field,
                "requirement": requirement,
                "value": value,
                "message": message
            })

        # -----------------------------------------------------
        # POTENTIAL NON-COMPLIANCE
        # -----------------------------------------------------

        elif status == "POTENTIAL_NON_COMPLIANCE":
            violations.append({
                "field": field,
                "requirement": requirement,
                "value": value,
                "expected": check.get("expected"),
                "message": message
            })

        # -----------------------------------------------------
        # MISSING DECLARATION
        # -----------------------------------------------------

        elif status == "NOT_FOUND":
            violations.append({
                "field": field,
                "requirement": requirement,
                "value": None,
                "expected": requirement,
                "message": message
            })

        # -----------------------------------------------------
        # QR REFERENCED
        # -----------------------------------------------------

        elif status == "QR_REFERENCED":
            reviews.append({
                "field": field,
                "requirement": requirement,
                "value": value,
                "message": message
            })

        # -----------------------------------------------------
        # VISUAL ANALYSIS
        # -----------------------------------------------------

        elif status == "PENDING_VISUAL_ANALYSIS":
            reviews.append({
                "field": field,
                "requirement": requirement,
                "value": value,
                "message": message
            })

        # -----------------------------------------------------
        # UNABLE TO VALIDATE
        # -----------------------------------------------------

        elif status == "UNABLE_TO_VALIDATE":
            reviews.append({
                "field": field,
                "requirement": requirement,
                "value": value,
                "message": message
            })

    # ---------------------------------------------------------
    # OVERALL STATUS
    # ---------------------------------------------------------

    if violations:
        overall_status = "POTENTIAL_NON_COMPLIANCE"

    elif reviews:
        overall_status = "REVIEW_REQUIRED"

    else:
        overall_status = "NO_DETECTED_VIOLATIONS"

    return {
        "overall_status": overall_status,
        "violations": violations,
        "warnings": warnings,
        "passed": passed,
        "reviews": reviews,
        "summary": {
            "violations": len(violations),
            "warnings": len(warnings),
            "passed": len(passed),
            "reviews": len(reviews)
        }
    }