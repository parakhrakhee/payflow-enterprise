import csv
from pathlib import Path

from payflow.pipeline import run_pipeline


def test_pipeline_writes_accepted_and_rejected_csv_files(tmp_path):
    project_root = Path(__file__).resolve().parents[2]
    input_path = project_root / "data" / "samples" / "payments.csv"

    counts = run_pipeline(input_path, tmp_path)

    assert counts == {"accepted_count": 3, "rejected_count": 6}

    accepted_path = tmp_path / "accepted_payments.csv"
    rejected_path = tmp_path / "rejected_payments.csv"

    assert accepted_path.exists()
    assert rejected_path.exists()

    with accepted_path.open(newline="", encoding="utf-8") as file:
        accepted_rows = list(csv.DictReader(file))

    with rejected_path.open(newline="", encoding="utf-8") as file:
        rejected_rows = list(csv.DictReader(file))

    assert len(accepted_rows) == 3
    assert len(rejected_rows) == 6
    assert "reason" in rejected_rows[0]
