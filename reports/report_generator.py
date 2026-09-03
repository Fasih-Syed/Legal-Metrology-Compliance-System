from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from PIL import Image as PILImage
from datetime import datetime


def generate_report(
    declarations,
    compliance_result,
    violation_result,
    image_quality,
    qr_result,
    image_bytes=None
):
    """
    Generate a PDF compliance inspection report.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    story = []

    # ------------------------------------------
    # TITLE
    # ------------------------------------------

    story.append(
        Paragraph(
            "LEGAL METROLOGY<br/>COMPLIANCE REPORT",
            title_style
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"Inspection Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    # ------------------------------------------
    # PRODUCT IMAGE
    # ------------------------------------------

    if image_bytes:

        try:
            image_buffer = BytesIO(image_bytes)

            product_image = Image(
                image_buffer,
                width=3.0 * inch,
                height=4.0 * inch
            )

            story.append(product_image)
            story.append(Spacer(1, 15))

        except Exception:
            pass

    # ------------------------------------------
    # OVERALL STATUS
    # ------------------------------------------

    status = violation_result.get(
        "overall_status",
        compliance_result.get(
            "overall_status",
            "REVIEW_REQUIRED"
        )
    )

    story.append(
        Paragraph(
            f"<b>Overall Status:</b> {status}",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 10))

    # ------------------------------------------
    # EXTRACTED DECLARATIONS
    # ------------------------------------------

    story.append(
        Paragraph(
            "Extracted Product Declarations",
            styles["Heading2"]
        )
    )

    declaration_data = [
        ["Field", "Detected Value"]
    ]

    for key, value in declarations.items():

        if value is not None:

            declaration_data.append([
                key.replace("_", " ").title(),
                str(value)
            ])

    declaration_table = Table(
        declaration_data,
        colWidths=[2.0 * inch, 4.5 * inch]
    )

    declaration_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    story.append(declaration_table)
    story.append(Spacer(1, 20))

    # ------------------------------------------
    # COMPLIANCE CHECKS
    # ------------------------------------------

    story.append(
        Paragraph(
            "Compliance Checks",
            styles["Heading2"]
        )
    )

    checks = compliance_result.get(
        "checks",
        {}
    )

    check_data = [
        ["Requirement", "Status", "Message"]
    ]

    for name, result in checks.items():

        if isinstance(result, dict):

            check_data.append([
                name.replace("_", " ").title(),
                str(result.get("status", "UNKNOWN")),
                str(result.get("message", ""))
            ])

    check_table = Table(
        check_data,
        colWidths=[
            1.5 * inch,
            1.2 * inch,
            3.8 * inch
        ]
    )

    check_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
        ])
    )

    story.append(check_table)
    story.append(Spacer(1, 20))

    # ------------------------------------------
    # VIOLATIONS
    # ------------------------------------------

    story.append(
        Paragraph(
            "Violations",
            styles["Heading2"]
        )
    )

    violations = violation_result.get(
        "violations",
        []
    )

    if violations:

        for violation in violations:

            story.append(
                Paragraph(
                    f"• {violation}",
                    styles["Normal"]
                )
            )

    else:

        story.append(
            Paragraph(
                "No violations detected.",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 15))

    # ------------------------------------------
    # REVIEW ITEMS
    # ------------------------------------------

    story.append(
        Paragraph(
            "Review Required",
            styles["Heading2"]
        )
    )

    reviews = violation_result.get(
        "reviews",
        []
    )

    if reviews:

        for review in reviews:

            story.append(
                Paragraph(
                    f"• {review}",
                    styles["Normal"]
                )
            )

    else:

        story.append(
            Paragraph(
                "No additional review items.",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 15))

    # ------------------------------------------
    # IMAGE QUALITY
    # ------------------------------------------

    story.append(
        Paragraph(
            "Image Quality Analysis",
            styles["Heading2"]
        )
    )

    if isinstance(image_quality, dict):

        quality_data = [
            ["Metric", "Value"],
            [
                "Status",
                str(image_quality.get("status", "UNKNOWN"))
            ],
            [
                "Contrast",
                str(image_quality.get("contrast", "N/A"))
            ],
            [
                "Sharpness",
                str(image_quality.get("sharpness", "N/A"))
            ],
            [
                "Brightness",
                str(image_quality.get("brightness", "N/A"))
            ]
        ]

        quality_table = Table(
            quality_data,
            colWidths=[2.5 * inch, 3.5 * inch]
        )

        quality_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ])
        )

        story.append(quality_table)

    story.append(Spacer(1, 20))

    # ------------------------------------------
    # QR ANALYSIS
    # ------------------------------------------

    story.append(
        Paragraph(
            "QR Code Analysis",
            styles["Heading2"]
        )
    )

    qr_status = qr_result.get(
        "status",
        "NOT_FOUND"
    )

    story.append(
        Paragraph(
            f"<b>Status:</b> {qr_status}",
            styles["Normal"]
        )
    )

    if qr_result.get("data"):

        story.append(
            Paragraph(
                f"<b>QR Data:</b> {qr_result['data']}",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            "Generated by AI-assisted Legal Metrology "
            "Compliance System",
            styles["Normal"]
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()