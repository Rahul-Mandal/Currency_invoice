from pydantic import BaseModel, Field
from typing import List, Optional

class Invoice(BaseModel):
    """Model for an individual invoice."""

    id: str
    amount: float
    currency: str
    customer: str

class InvoiceRequest(BaseModel):
    """Model for the request payload."""

    invoices: List[Invoice]

class ConvertedInvoice(BaseModel):
    """Model for a single converted invoice."""
    
    id: str
    original: str
    converted: str

class InvalidInvoice(BaseModel):
    """Model for invalid invoices."""
    id: str
    error: str

class InvoiceReport(BaseModel):
    """Model for the summary report."""
    total_invoices: int
    total_amount_usd: float
    invalid_invoices: List[InvalidInvoice]
    converted: List[ConvertedInvoice]
