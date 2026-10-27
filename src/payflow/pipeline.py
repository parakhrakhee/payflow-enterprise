import csv
from pathlib import Path

from payflow.validation import process_payments


ACCEPTED_FIELDS = [
    "transaction_id",
    "customer_id",
    "amount",
    "currency",
    "status",
    "transaction_timestamp",
]

REJECTED_FIELDS = ["transaction_id", "reason"]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    """Write records to a CSV file, including a header for empty outputs."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_pipeline(input_path: Path, output_dir: Path) -> dict[str, int]:
    """Validate payment records and persist accepted/rejected outputs."""
    accepted, rejected = process_payments(input_path)

    write_csv(output_dir / "accepted_payments.csv", ACCEPTED_FIELDS, accepted)
    write_csv(output_dir / "rejected_payments.csv", REJECTED_FIELDS, rejected)

    return {
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
    }
