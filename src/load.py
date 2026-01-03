import os
import logging
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine, text


def load_to_sql_server(df: pd.DataFrame):
    """Loads transformed sales data into SQL Server staging table.

    Defaults match the screenshot: Server=`BUNY`, Database=`sales_dw`,
    Windows Authentication (Trusted Connection).

    Connection settings may be overridden with environment variables:
      - SQL_SERVER (default: BUNY)
      - SQL_DATABASE (default: sales_dw)
      - SQL_DRIVER (default: ODBC Driver 17 for SQL Server)
      - SQL_TRUSTED (default: yes)
      - SQL_USER, SQL_PASSWORD (used when SQL_TRUSTED is false)
    """
    logging.info("[LOAD] Starting data load into SQL Server")

    server = os.getenv("SQL_SERVER", "BUNY")
    database = os.getenv("SQL_DATABASE", "sales_dw")
    driver = os.getenv("SQL_DRIVER", "ODBC Driver 17 for SQL Server")
    trusted = os.getenv("SQL_TRUSTED", "yes").lower() in ("1", "true", "yes", "y")
    user = os.getenv("SQL_USER")
    password = os.getenv("SQL_PASSWORD")

    if trusted:
        conn_str = f"DRIVER={{{driver}}};Server={server};Database={database};Trusted_Connection=yes;"
    else:
        if not (user and password):
            logging.error("[LOAD] SQL_USER and SQL_PASSWORD must be set when SQL_TRUSTED is false")
            raise ValueError("Missing SQL credentials")
        conn_str = f"DRIVER={{{driver}}};Server={server};Database={database};UID={user};PWD={password};"

    logging.info(f"[LOAD] Using server={server} database={database} trusted={trusted}")

    quoted = quote_plus(conn_str)
    engine_url = f"mssql+pyodbc:///?odbc_connect={quoted}"

    try:
        engine = create_engine(engine_url, fast_executemany=True)
    except Exception:
        logging.exception("[LOAD] Failed to create SQLAlchemy engine")
        # fallback: write CSV for manual inspection
        _write_fallback_csv(df, reason="engine_creation_failed")
        raise

    try:
        # Map DataFrame columns (often UPPERCASE) to database snake_case column names
        col_mapping = {
            "ORDERNUMBER": "order_number",
            "QUANTITYORDERED": "quantity_ordered",
            "PRICEEACH": "price_each",
            "ORDERLINENUMBER": "order_line_number",
            "SALES": "sales",
            "ORDERDATE": "order_date",
            "DAYS_SINCE_LASTORDER": "days_since_last_order",
            "STATUS": "status",
            "PRODUCTLINE": "product_line",
            "MSRP": "msrp",
            "PRODUCTCODE": "product_code",
            "CUSTOMERNAME": "customer_name",
            "PHONE": "phone",
            "ADDRESSLINE1": "address_line1",
            "CITY": "city",
            "POSTALCODE": "postal_code",
            "COUNTRY": "country",
            "CONTACTLASTNAME": "contact_last_name",
            "CONTACTFIRSTNAME": "contact_first_name",
            "DEALSIZE": "deal_size",
            # already-lower columns
            "order_year": "order_year",
            "order_month": "order_month",
            "revenue_bucket": "revenue_bucket",
            "load_timestamp": "load_timestamp",
        }

        df_for_db = df.copy()
        # rename only columns that exist in the DataFrame
        rename_map = {k: v for k, v in col_mapping.items() if k in df_for_db.columns}
        if rename_map:
            df_for_db = df_for_db.rename(columns=rename_map)

        # Align DataFrame columns to the table column order (add missing columns as NULL)
        with engine.connect() as conn:
            res = conn.execute(
                text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'stg_sales_orders' ORDER BY ORDINAL_POSITION")
            )
            table_cols = [row[0] for row in res.fetchall()]

        # Reindex DataFrame to match table columns; missing columns become NaN
        common_cols = [c for c in table_cols if c in df_for_db.columns]
        df_for_db = df_for_db.reindex(columns=table_cols)

        df_for_db.to_sql(name="stg_sales_orders", con=engine, if_exists="append", index=False)
        logging.info("[LOAD] Data successfully loaded into stg_sales_orders")
    except Exception:
        logging.exception("[LOAD] Failed to write dataframe to SQL Server; writing fallback CSV")
        _write_fallback_csv(df, reason="to_sql_failed")
        raise


def _write_fallback_csv(df: pd.DataFrame, reason: str):
    out_dir = Path("sales_data_pipeline/failed_load")
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = out_dir / f"sales_orders_failed_load_{reason}.csv"
    try:
        df.to_csv(fname, index=False)
        logging.info(f"[LOAD] Wrote fallback CSV: {fname}")
    except Exception:
        logging.exception("[LOAD] Failed to write fallback CSV")