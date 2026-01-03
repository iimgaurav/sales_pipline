import pandas as pd
from src.validate import validate_sales_data


def make_sample_df():
    return pd.DataFrame(
        {
            "ORDERNUMBER": [1, None, 3],
            "ORDERDATE": ["01/01/2020", "02/02/2020", "03/03/2020"],
            "SALES": [100.0, 200.0, None],
            "PRODUCTCODE": ["S1", "S2", "S3"],
            "CUSTOMERNAME": ["A", "B", "C"],
        }
    )


def test_validate_splits_valid_and_rejected():
    df = make_sample_df()
    valid, rejected = validate_sales_data(df)
    # Expect some rejected rows due to nulls
    assert isinstance(valid, pd.DataFrame)
    assert isinstance(rejected, pd.DataFrame)
    assert len(rejected) >= 1
