import logging
from pathlib import Path
try:
    # When running from project root with src on PYTHONPATH
    from src.extract import read_raw_sales_data
    from src.validate import validate_sales_data
    from src.transform import transform_sales_data
    from src.load import load_to_sql_server
except ModuleNotFoundError:
    # When running from the `src/` directory directly
    from extract import read_raw_sales_data
    from validate import validate_sales_data
    from transform import transform_sales_data
    from load import load_to_sql_server


def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_dir / "sales_pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def main():
    setup_logging()
    logging.info("[PIPELINE] Sales data pipeline started")

    raw_sales_df = read_raw_sales_data()
    valid_sales_df, rejected_sales_df = validate_sales_data(raw_sales_df)
    transformed_sales_df = transform_sales_data(valid_sales_df)

    load_to_sql_server(transformed_sales_df)

    logging.info("[PIPELINE] Data load completed successfully")


if __name__ == "__main__":
    main()
