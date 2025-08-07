from app.models import ConvertedInvoice, InvalidInvoice, InvoiceReport
from typing import List
from fpdf import FPDF
from pathlib import Path

# Define current_dir as a Path object
current_dir = Path(__file__).resolve().parent

# Use pathlib to build the file path
default_pdf_path = current_dir / "invoice_report.pdf"

def generate_report_json(
    converted: List[ConvertedInvoice],
    invalid: List[InvalidInvoice]
) -> InvoiceReport:
    """Generates a summary report in JSON format."""

    print(converted, '=====')
    total = sum(float(inv['converted'].split()[0]) for inv in converted)
    print(total, 'total----')
    return InvoiceReport(
        total_invoices=len(converted+invalid),
        total_amount_usd=total,
        invalid_invoices=invalid,
        converted=converted
    )

def generate_pdf(report: InvoiceReport, file_path: str = default_pdf_path):
    """Generates a PDF report from the JSON data."""

    # If no file_path is provided, use the default
    if file_path is None:
        file_path = str(default_pdf_path)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Invoice Report", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Total Invoices: {report.total_invoices}", ln=True)
    pdf.cell(200, 10, txt=f"Total Amount (USD): {report.total_amount_usd}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Converted Invoices:", ln=True)
    for inv in report.converted:
        pdf.cell(200, 10, txt=f"{inv.id}: {inv.original} -> {inv.converted}", ln=True)


    if report.invalid_invoices:
        pdf.ln(10)
        pdf.cell(200, 10, txt="Invalid Invoices:", ln=True)
        for inv in report.invalid_invoices:
            pdf.cell(200, 10, txt=f"{inv.id}: {inv.error}", ln=True)


    pdf.output(file_path)
