import unittest
from pathlib import Path

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
import os

from pdfClass import PDF

class TestOCRPDF(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Create a proper non-searchable invoice PDF with correct table formatting"""
        cls.test_pdf_path = "test_invoice.pdf"
        cls.output_pdf_path = "test_output.pdf"

        cls.expected_text = [
            "Invoice No:", "12345",
            "Bill To:", "John Doe",
            "Company:", "ABC Corp.",
            "Date:", "2025-02-15",
            "Item", "Qty", "Unit Price", "Total",
            "Laptop", "1", "$1000", "$1000",
            "Mouse", "2", "$50", "$100",
            "Total:", "$1100"
        ]

        # **Step 1: Create a Proper Invoice PDF Using Table**
        invoice_pdf = "invoice_temp.pdf"
        doc = SimpleDocTemplate(invoice_pdf, pagesize=letter)

        # Invoice Header
        invoice_data = [
            ["Invoice No:", "12345"],
            ["Bill To:", "John Doe"],
            ["Company:", "ABC Corp."],
            ["Date:", "2025-02-15"]
        ]

        table_data = [
            ["Item", "Qty", "Unit Price", "Total"],
            ["Laptop", "1", "$1000", "$1000"],
            ["Mouse", "2", "$50", "$100"],
            ["", "", "Total:", "$1100"]
        ]

        # Table Styling
        style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])

        invoice_table = Table(invoice_data)
        items_table = Table(table_data)
        items_table.setStyle(style)

        # Build PDF
        doc.build([invoice_table, items_table])

        # **Step 2: Convert the PDF to an Image (Simulating a Scan)**
        doc = fitz.open(invoice_pdf)
        pix = doc[0].get_pixmap(dpi=300)
        img_path = "invoice_image.png"
        Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(img_path)
        doc.close()

        # **Step 3: Create a Non-Searchable PDF from the Image**
        doc = fitz.open()
        page = doc.new_page(width=pix.width, height=pix.height)
        rect = fitz.Rect(0, 0, pix.width, pix.height)
        page.insert_image(rect, filename=img_path)
        doc.save(cls.test_pdf_path)
        doc.close()


    def test_ocr_conversion(self):
        """Test if OCR function correctly makes the invoice searchable"""
        pdf_obj = PDF(Path(self.test_pdf_path))
        pdf_obj.ocr()

        # Open the output PDF and extract text
        doc = fitz.open(self.test_pdf_path)
        extracted_text = ""
        for page in doc:
            extracted_text += page.get_text()
        doc.close()

        # Assert that every expected element is present in the OCR result
        for text in self.expected_text:
            self.assertIn(text, extracted_text, f"Missing text: {text}")

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary test files"""
        os.remove(cls.test_pdf_path)
        os.remove("invoice_temp.pdf")
        os.remove("invoice_image.png")

if __name__ == "__main__":
    unittest.main()