import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


ALLOWED_CURRENCIES = {"USD"}
ALLOWED_STATUSES = {"COMPLETED", "PENDING"}

REQUIRED_FIELDS = {
    "transaction_id",
    "customer_id",
    "amount",
    "currency",
    "status",
    "transaction_timestamp",
}


def validate_payment(row: dict[str, str]) -> list[str]:
    """Return validation errors for one payment record."""
    errors = []

    if not REQUIRED_FIELDS.issubset(row.keys()):
        return ["Missing required columns"]

    for field in REQUIRED_FIELDS:
        if not (row.get(field) or "").strip():
            errors.append(f"Missing required value: {field}")

    if errors:
        return errors

    try:
        amount = Decimal(row["amount"])
        if not amount.is_finite():
            errors.append("Amount must be a finite number")
        elif amount <= 0:
            errors.append("Amount must be greater than zero")
    except InvalidOperation:
        errors.append("Amount must be numeric")

    if row["currency"].strip() not in ALLOWED_CURRENCIES:
        errors.append("Unsupported currency")

    if row["status"].strip() not in ALLOWED_STATUSES:
        errors.append("Unsupported status")

    try:
        timestamp = row["transaction_timestamp"].strip()
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        errors.append("Invalid transaction timestamp")

    return errors


def process_payments(input_path: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Return accepted payments and rejected records with reasons."""
    accepted = []
    rejected = []
    seen_transaction_ids = set()

    with input_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        if not reader.fieldnames or not REQUIRED_FIELDS.issubset(reader.fieldnames):
            raise ValueError("Input CSV is missing required columns")

        for row in reader:
            errors = validate_payment(row)

            if errors:
                rejected.append({
                    "transaction_id": row.get("transaction_id") or "",
                    "reason": "; ".join(errors),
                })
                continue

            transaction_id = row["transaction_id"].strip()

            if transaction_id in seen_transaction_ids:
                rejected.append({
                    "transaction_id": transaction_id,
                    "reason": "Duplicate transaction ID",
                })
                continue

            seen_transaction_ids.add(transaction_id)
            accepted.append(row)

    return accepted, rejected
