import streamlit as st

from reports.report_generator import generate_report
from image_processing.preprocessing import preprocess_image
from ocr.ocr_engine import extract_text
from declaration.declaration_extractor import extract_declarations
from compliance.rule_engine import check_required_declarations
from compliance.violation_detector import detect_violations
from visual_analysis.readability import calculate_image_quality
from qr_analysis.qr_scanner import scan_qr_code


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Legal Metrology Compliance System",
    page_icon="⚖️",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("⚖️ Legal Metrology Compliance System")

st.write(
    "AI-assisted inspection of packaged commodities "
    "under Legal Metrology requirements."
)

st.divider()


# --------------------------------------------------
# IMAGE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a packaged commodity image",
    type=["jpg", "jpeg", "png"]
)


# --------------------------------------------------
# PROCESS IMAGE
# --------------------------------------------------

if uploaded_file is not None:

    st.subheader("📷 Product Image")

    st.image(
        uploaded_file,
        caption="Uploaded Product",
        use_container_width=True
    )

    if st.button("🔍 Scan Product", type="primary"):

        with st.spinner("Analyzing product..."):

            # ------------------------------------------
            # 1. PREPROCESSING
            # ------------------------------------------

            processed_image, _ = preprocess_image(
                uploaded_file
            )

            # ------------------------------------------
            # 2. OCR
            # ------------------------------------------

            ocr_text = extract_text(
                processed_image
            )

            # ------------------------------------------
            # 3. DECLARATION EXTRACTION
            # ------------------------------------------

            declarations = extract_declarations(
                ocr_text
            )

            # ------------------------------------------
            # 4. COMPLIANCE CHECK
            # ------------------------------------------

            compliance_result = check_required_declarations(
    declarations
)
            

            # ------------------------------------------
            # 5. VIOLATION DETECTION
            # ------------------------------------------

            violation_result = detect_violations(
                compliance_result
            )

            # ------------------------------------------
            # 6. IMAGE QUALITY
            # ------------------------------------------

            image_quality = calculate_image_quality(
                processed_image
            )

                      # ------------------------------------------
            # 7. QR ANALYSIS
            # ------------------------------------------

            qr_result = scan_qr_code(
                processed_image
            )

        # ------------------------------------------
        # INSPECTION REPORT
        # ------------------------------------------

        st.divider()

        st.subheader("📄 Inspection Report")

        report = generate_report(
            declarations=declarations,
            compliance_result=compliance_result,
            violation_result=violation_result,
            image_quality=image_quality,
            qr_result=qr_result,
            image_bytes=uploaded_file.getvalue()
        )

        st.download_button(
            label="📥 Download Compliance Report",
            data=report,
            file_name="legal_metrology_compliance_report.pdf",
            mime="application/pdf"
        )

        # ==================================================
        # RESULTS
        # ==================================================

        st.success("Product analysis completed.")

        st.divider()

        # --------------------------------------------------
        # OVERALL STATUS
        # --------------------------------------------------

        st.subheader("📊 Compliance Summary")

        status = violation_result.get(
            "overall_status",
            compliance_result.get(
                "overall_status",
                "REVIEW_REQUIRED"
            )
        )

        summary = violation_result.get(
            "summary",
            {}
        )

        passed = summary.get("passed", 0)
        violations_count = summary.get("violations", 0)
        warnings_count = summary.get("warnings", 0)
        reviews_count = summary.get("reviews", 0)

        if status == "COMPLIANT":
            st.success("✅ PRODUCT APPEARS COMPLIANT")
        elif status == "POTENTIAL_NON_COMPLIANCE":
            st.error("❌ POTENTIAL NON-COMPLIANCE DETECTED")
        else:
            st.warning("⚠️ REVIEW REQUIRED")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("✅ Passed", passed)

        with col2:
            st.metric("❌ Violations", violations_count)

        with col3:
            st.metric("⚠️ Warnings", warnings_count)

        with col4:
            st.metric("🔎 Review", reviews_count)

        st.divider()

        # --------------------------------------------------
        # DECLARATIONS
        # --------------------------------------------------

        st.subheader("📋 Extracted Declarations")

        for key, value in declarations.items():
            if value is not None:
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")

        st.divider()

        # --------------------------------------------------
        # COMPLIANCE CHECKS
        # --------------------------------------------------

        st.subheader("⚖️ Compliance Checks")

        checks = compliance_result.get("checks", {})

        for name, result in checks.items():
            if isinstance(result, dict):
                check_status = result.get("status", "UNKNOWN")
                message = result.get("message", "")
            else:
                check_status = "UNKNOWN"
                message = str(result)

            if check_status == "FOUND":
                st.success(f"✅ **{name}** — {message}")
            elif check_status == "VALID":
                st.success(f"✅ **{name}** — {message}")
            elif check_status == "NOT_FOUND":
                st.error(f"❌ **{name}** — {message}")
            else:
                st.warning(f"⚠️ **{name}** — {message}")

        st.divider()

        # --------------------------------------------------
        # VIOLATIONS
        # --------------------------------------------------

        st.subheader("🚨 Violations & Review Items")

        violations = violation_result.get("violations", [])
        reviews = violation_result.get("reviews", [])

        if violations:
            for item in violations:
                if isinstance(item, dict):
                    field = item.get("field", "Unknown")
                    message = item.get("message", "")

                    st.error(
                        f"❌ **{field.replace('_', ' ').title()}** — {message}"
                    )
                else:
                    st.error(f"❌ {item}")

        if reviews:
            for item in reviews:
                if isinstance(item, dict):
                    field = item.get("field", "Unknown")
                    message = item.get("message", "")

                    st.warning(
                        f"⚠️ **{field.replace('_', ' ').title()}** — {message}"
                    )
                else:
                    st.warning(f"⚠️ {item}")

        if not violations and not reviews:
            st.success("No violations or review items detected.")

        st.divider()

        # --------------------------------------------------
        # IMAGE QUALITY
        # --------------------------------------------------

        st.subheader("🖼️ Image Quality Analysis")

        if isinstance(image_quality, dict):
            quality_col1, quality_col2, quality_col3 = st.columns(3)

            with quality_col1:
                st.metric(
                    "Status",
                    image_quality.get("status", "UNKNOWN")
                )

            with quality_col2:
                st.metric(
                    "Contrast",
                    round(image_quality.get("contrast", 0), 2)
                )

            with quality_col3:
                st.metric(
                    "Sharpness",
                    round(image_quality.get("sharpness", 0), 2)
                )

        # --------------------------------------------------
        # QR CODE
        # --------------------------------------------------

        st.subheader("🔳 QR Code Analysis")

        qr_status = qr_result.get("status", "NOT_FOUND")

        if qr_status == "FOUND":

            st.success("✅ QR code detected and decoded.")

            st.write(
                f"**QR Data:** {qr_result.get('data')}"
            )

        elif qr_status == "DETECTED_NOT_READABLE":

            st.warning(
                "⚠️ QR code detected, but its contents "
                "could not be decoded. Manual verification required."
            )

        else:

            st.info(
                "ℹ️ No readable QR code was detected in the image."
            )