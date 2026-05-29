import pandas as pd
import pytest

from io import BytesIO
from app.api.services.clean_data import clean_and_format_csv
#Tests :  error dates more than 10% of the dataset

def bad_csv():
    return b'\xff\xfe'

def empty_csv():
    empty = pd.DataFrame(
        {
            "Order ID": [],
            "Order Date": [],
            "Order Status": [],
            "Product SKU": [],
            "Product Name": [],
            "Price": [],
            "Qty Ordered": [],
        }
    )
    return empty.to_csv(index=False).encode()

def missing_columns_csv():
    #Missing price column
    missing_column = pd.DataFrame(
        {
            "Order ID": [34554,45665,5433],
            "Order Date": ["2026-05-15 13:48:00", "2026-05-10 13:50:00", "2026-05-20 15:48:00"],
            "Order Status": ["processing", "complete", "pending"],
            "Product SKU": ["GHY/0LM8/10-f","GHY/0LM8/10-f","GHY/0LM8/10-f"],
            "Product Name": ["Velvet", "Satin", "Black Satin"],
            "Qty Ordered": [4,3,2],  
        }
    )
    return missing_column.to_csv(index=False).encode()

def bad_dates_csv():
    bad_dates = pd.DataFrame(
        {
            "Order ID": [34554,45665,5433],
            "Order Date": ["2026-05-15 13:48:00", "no date :( ", "missing!!!!"],
            "Order Status": ["processing", "complete", "pending"],
            "Product SKU": ["GHY/0LM8/10-f","GHY/0LM8/10-f","GHY/0LM8/10-f"],
            "Product Name": ["Velvet", "Satin", "Black Satin"],
            "Price": [4.5, 5.5, 5.5],
            "Qty Ordered": [4, 3, 2], 
        }
    )
    return bad_dates.to_csv(index=False).encode()

def test_bad_csv():
    with pytest.raises(ValueError) as e:
        clean_and_format_csv(bad_csv())
    assert "Could not parse CSV file" in str(e.value)

def test_empty_csv():
    with pytest.raises(ValueError) as e:
        clean_and_format_csv(empty_csv())
    assert "CSV file is empty" in str(e.value)

def test_missing_columns():
    with pytest.raises(ValueError) as e:
        clean_and_format_csv(missing_columns_csv())
    assert "Column Price missing from data"

def test_bad_dates():
    with pytest.raises(ValueError) as e:
        clean_and_format_csv(bad_dates_csv())
    assert "Too many null dates" in str(e.value)