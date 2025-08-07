from http.client import HTTPException
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

from app.models import InvoiceRequest
from app.validators import validate_invoices
from app.currency_converter import fetch_exchange_rates, convert_to_usd
from app.report_generator import generate_report_json, generate_pdf

app = FastAPI()

@app.post("/process-invoices")
async def process_invoices(payload: InvoiceRequest):
    """
    Processes the invoices, validates them, converts amounts to USD, 
    and generates a summary report.
    
    - Accepts a list of invoices for currency conversion.
    - Returns a report with valid invoices converted to USD.
    """
    # Validate Invoices
    valid, invalid = validate_invoices(payload.invoices)

    # Validate fetch_exchange_rates
    print(valid)
    print(invalid)
    currencies = set(inv.currency for inv in valid)
    rates = await fetch_exchange_rates(currencies)

    # Convert Invoices
    converted = []
    for inv in valid:
        rate = rates.get(inv.currency)
        if rate:
            usd_amount = convert_to_usd(inv.amount, rate)
            converted.append({
                "id": inv.id,
                "original": f"{inv.amount} {inv.currency}",
                "converted": f"{usd_amount} USD"
            })
    
    # Generate JSON and PDF Report
    report = generate_report_json(converted, invalid)
    generate_pdf(report)  # Optional
    return report.dict()


@app.get("/download-pdf")
def download_pdf():
    """
    download pdf 
    """

    pdf_path = Path(__file__).parent / "invoice_report.pdf"
    return FileResponse(
        path=pdf_path,
        filename="invoice_report.pdf",
        media_type="application/pdf"
    )

