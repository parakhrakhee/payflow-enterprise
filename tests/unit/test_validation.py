from decimal import Decimal

from payflow.validation import process_payments, validate_payment


def valid_payment():
    return {
        "transaction_id": "TXN2001",
        "customer_id": "CUST201",
        "amount": "49.99",
        "currency": "USD",
        "status": "COMPLETED",
        "transaction_timestamp": "2026-10-26T10:15:00Z",
    }


def test_valid_payment_is_accepted_by_validator():
    assert validate_payment(valid_payment()) == []


def test_zero_amount_is_rejected():
    row = valid_payment()
    row["amount"] = "0"

    assert "Amount must be greater than zero" in validate_payment(row)


def test_negative_amount_is_rejected():
    row = valid_payment()
    row["amount"] = "-12.00"

    assert "Amount must be greater than zero" in validate_payment(row)


def test_nonnumeric_amount_is_rejected():
    row = valid_payment()
    row["amount"] = "abc"

    assert "Amount must be numeric" in validate_payment(row)


def test_unsupported_currency_is_rejected():
    row = valid_payment()
    row["currency"] = "XYZ"

    assert "Unsupported currency" in validate_payment(row)


def test_missing_customer_id_is_rejected():
    row = valid_payment()
    row["customer_id"] = ""

    assert "Missing required value: customer_id" in validate_payment(row)


def test_pending_status_is_allowed():
    row = valid_payment()
    row["status"] = "PENDING"

    assert validate_payment(row) == []


def test_duplicate_transaction_id_is_rejected(tmp_path):
    import csv

    first = valid_payment()
    duplicate = valid_payment()

    input_path = tmp_path / "payments.csv"
    with input_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=first.keys())
        writer.writeheader()
        writer.writerow(first)
        writer.writerow(duplicate)

    accepted, rejected = process_payments(input_path)

    assert len(accepted) == 1
    assert len(rejected) == 1
    assert rejected[0]["reason"] == "Duplicate transaction ID"


def test_sample_dataset_has_expected_counts():
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    input_path = project_root / "data" / "samples" / "payments.csv"

    accepted, rejected = process_payments(input_path)

    assert len(accepted) == 3
    assert len(rejected) == 6

def test_invalid_timestamp_is_rejected():
    row = valid_payment()
    row["transaction_timestamp"] = "not-a-timestamp"

    assert "Invalid transaction timestamp" in validate_payment(row)


def test_missing_required_column_is_rejected():
    row = valid_payment()
    del row["customer_id"]

    assert validate_payment(row) == ["Missing required columns"]


def test_non_finite_amount_is_rejected():
    row = valid_payment()
    row["amount"] = "NaN"

    assert "Amount must be a finite number" in validate_payment(row)


def test_whitespace_only_transaction_id_is_rejected():
    row = valid_payment()
    row["transaction_id"] = "   "

    assert "Missing required value: transaction_id" in validate_payment(row)