import pandas as pd 
import logging
from pathlib import Path

RAW_DATA_PATH = Path("sales_data_pipeline/raw/Auto Sales data.csv")

def read_raw_sales_data() -> pd.DataFrame:
    """
    Reads raw sales data from CSV file.
    Returns a pandas DataFrame.
    """
    logging.info("[EXTRACT] Starting raw data ingestion")

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Source file not found: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)

    if df.empty:
        raise ValueError("Raw sales file is empty")

    logging.info(
        f"[EXTRACT] Raw data loaded successfully | Rows: {df.shape[0]} | Columns: {df.shape[1]}"
    )

    return df