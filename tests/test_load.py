import pandas as pd
import os
from pathlib import Path
from src.load import _write_fallback_csv


def test_write_fallback_csv_creates_file(tmp_path, monkeypatch):
    # Prepare a small DataFrame
    df = pd.DataFrame({"A": [1, 2, 3]})
    # Use temp directory for output
    monkeypatch.chdir(tmp_path)
    _write_fallback_csv(df, reason="unit_test")
    out_dir = Path("sales_data_pipeline/failed_load")
    files = list(out_dir.glob("sales_orders_failed_load_unit_test*.csv"))
    assert len(files) == 1
    # cleanup
    for f in files:
        f.unlink()
