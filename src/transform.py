import pandas as pd
import logging
from datetime import datetime
import uuid


def generate_batch_id() -> str:
    """Generate unique batch ID for tracking data loads"""
    return f"SALES_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"


def transform_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies business transformations to validated sales data.
    Returns transformed DataFrame.
    """
    logging.info("[TRANSFORM] Starting business transformations")

    transformed_df = df.copy()

    # Text standardization
    transformed_df["COUNTRY"] = transformed_df["COUNTRY"].str.upper().str.strip()
    transformed_df["CITY"] = transformed_df["CITY"].str.title().str.strip()
    transformed_df["DEALSIZE"] = transformed_df["DEALSIZE"].str.upper().str.strip()
    transformed_df["STATUS"] = transformed_df["STATUS"].str.upper().str.strip()

    # Derived date columns
    transformed_df["order_year"] = transformed_df["ORDERDATE"].dt.year
    transformed_df["order_month"] = transformed_df["ORDERDATE"].dt.month

    # Revenue bucket (business logic)
    def revenue_bucket(sales):
        if sales < 3000:
            return "LOW"
        elif sales < 6000:
            return "MEDIUM"
        else:
            return "HIGH"

    transformed_df["revenue_bucket"] = transformed_df["SALES"].apply(revenue_bucket)

    # Generate batch ID for this load
    batch_id = generate_batch_id()
    transformed_df["batch_id"] = batch_id
    
    # Audit column - store as datetime object without timezone
    transformed_df["load_timestamp"] = pd.Timestamp.now()
    
    # If you have source_file_name column
    transformed_df["source_file_name"] = "Auto Sales data.csv"

    logging.info(
        f"[TRANSFORM] Transformation completed | Batch ID: {batch_id} | Rows: {transformed_df.shape[0]}"
    )

    return transformed_df
