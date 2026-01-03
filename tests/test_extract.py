from src.extract import read_raw_sales_data


def test_read_raw_sales_data_returns_dataframe():
    df = read_raw_sales_data()
    # Should return a DataFrame
    assert hasattr(df, "shape")
    assert df.shape[1] > 0
