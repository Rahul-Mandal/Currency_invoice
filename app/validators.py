import pycountry
from typing import Tuple, List, Set, Dict
from app.models import Invoice, InvalidInvoice

def is_valid_currency(code: str) -> bool:
    return pycountry.currencies.get(alpha_3=code) is not None

def validate_invoices(invoices: List[Invoice]) -> Tuple[List[Invoice], List[InvalidInvoice]]:
    """Validates a list of invoices based on amount, currency, and unique ID."""

    seen_ids: Set[str] = set()
    valid_invoices: List[Invoice] = []
    invalid_invoices: List[InvalidInvoice] = []

    for inv in invoices:
        if inv.amount <= 0:
            invalid_invoices.append(InvalidInvoice(id=inv.id, error="Amount must be greater than 0"))
            continue
        if not is_valid_currency(inv.currency):
            invalid_invoices.append(InvalidInvoice(id=inv.id, error="Currency code must be valid (ISO 4217 standard)"))
            continue
        if inv.id in seen_ids:
            invalid_invoices.append(InvalidInvoice(id=inv.id, error="Invoice ID must be unique"))
            continue

        seen_ids.add(inv.id)
        valid_invoices.append(inv)

    return valid_invoices, invalid_invoices
