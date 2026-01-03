import logging
from pathlib import Path
from typing import Tuple

import pandas as pd


CRITICAL_COLUMNS = [
    "ORDERNUMBER",
    "ORDERDATE",
    "SALES",
    "PRODUCTCODE",
    "CUSTOMERNAME",
]


def validate_sales_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Validates raw sales data and returns (valid_df, rejected_df)."""
    logging.info("[VALIDATION] Starting data validation")

    if df.empty:
        logging.info("[VALIDATION] Input dataframe is empty")
        return df.copy(), df.copy()

    # Null validation
    null_mask = df[CRITICAL_COLUMNS].isnull().any(axis=1)
    rejected_df = df[null_mask].copy()
    valid_df = df[~null_mask].copy()

    logging.info(f"[VALIDATION] Records rejected due to nulls: {rejected_df.shape[0]}")

    # Data type conversions (safe)
    try:
        if not valid_df.empty:
            valid_df["ORDERNUMBER"] = valid_df["ORDERNUMBER"].astype(int)
            if "QUANTITYORDERED" in valid_df.columns:
                valid_df["QUANTITYORDERED"] = valid_df["QUANTITYORDERED"].astype(int)
            if "PRICEEACH" in valid_df.columns:
                valid_df["PRICEEACH"] = valid_df["PRICEEACH"].astype(float)
            valid_df["SALES"] = valid_df["SALES"].astype(float)
            valid_df["ORDERDATE"] = pd.to_datetime(valid_df["ORDERDATE"], dayfirst=True)
    except Exception:
        logging.exception("[VALIDATION] Data type conversion failed")
        # Treat conversion failures as rejected records
        # Any rows that caused exceptions will be marked rejected
        # For simplicity, put all current valid_df into rejected
        rejected_df = pd.concat([rejected_df, valid_df], ignore_index=True)
        valid_df = df.iloc[0:0].copy()

    logging.info(f"[VALIDATION] Validation completed | Valid records: {valid_df.shape[0]}")
    return valid_df, rejected_df
