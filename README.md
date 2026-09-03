# ⚖️ Legal Metrology Compliance System

An AI-assisted system for analyzing packaged commodity labels and identifying potential compliance issues under Legal Metrology requirements.

## 🎯 Objective

The system accepts an image of a packaged commodity, extracts important declarations using OCR, checks them against predefined compliance requirements, identifies potential issues, and generates an inspection report.

## 🔄 System Workflow

```text
Product Image
     ↓
Image Preprocessing
     ↓
PaddleOCR
     ↓
Declaration Extraction
     ↓
Compliance Rule Engine
     ↓
Violation Detection
     ↓
Visual Analysis
     ↓
QR Code Analysis
     ↓
Compliance Dashboard
     ↓
PDF Inspection Report

✨ Features
📷 Packaged-product image upload
🔍 OCR-based text extraction
📋 Structured declaration extraction
⚖️ Compliance rule checking
🚨 Violation and review detection
💰 MRP and unit sale price validation
📦 Batch/lot identification
📅 Packing and use-by date extraction
🏢 Marketer and address extraction
📞 Customer-care information extraction
🔢 Barcode detection
🇮🇳 Country-of-origin detection
🔳 QR code analysis
🖼️ Image quality analysis
📊 Compliance dashboard
📄 Downloadable PDF inspection report
🧠 Technologies Used
Python — Core programming language
Streamlit — Web interface
PaddleOCR — Optical Character Recognition
OpenCV — Image processing and QR analysis
NumPy — Numerical/image processing operations
Pillow — Image handling
ReportLab — PDF report generation