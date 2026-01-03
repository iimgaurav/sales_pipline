import pandas as pd
from src.transform import transform_sales_data


def make_valid_df():
    return pd.DataFrame(
        {
            "COUNTRY": ["us", "uk"],
            "CITY": ["new york", "london"],
            "DEALSIZE": ["small", "large"],
            "STATUS": ["shipped", "pending"],
            "ORDERDATE": pd.to_datetime(["2020-01-01", "2020-02-01"]),
            "SALES": [1000, 7000],
        }
    )


def test_transform_adds_expected_columns():
    df = make_valid_df()
    out = transform_sales_data(df)
    assert "revenue_bucket" in out.columns
    assert "batch_id" in out.columns
    assert out["COUNTRY"].iloc[0] == "US"
