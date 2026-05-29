import json
import pandas as pd

# Test CSV file - Upload Endpoint
def valid_csv():
    test_csv = pd.DataFrame(
        {
            "Order ID": [2345, 2222, 3333 , 4523 , 4323, 4523, 4565, 5654, 56543, 54356],
            "Order Date": ["2026-05-15 13:48:00", "2026-05-10 13:50:00", "2026-05-20 15:48:00", "2026-08-29 19:58:16", "2026-11-07 16:12:05", "2026-12-31 23:40:27", "2026-03-02 17:45:39", "2026-07-05 06:37:42", "2026-11-07 16:12:05", "2026-12-31 23:40:27"],
            "Order Status": ["processing", "complete", "closed","processing", "complete", "closed","processing", "complete", "closed","processing"],
            "Product SKU": ["GHY/0LM8/10-f","GHY/0LM8/10-f","GHY/0LM8/10-f","GHY/0LM8/10-f","GHY/0LM8/10-f","GHY/0LM8/10-f","GHY/0LM8/10-f","GHY/0LM8/10-f","GHY/0LM8/10-f","GHY/0LM8/10-f"],
            "Product Name": ["Velvet", "Satin", "Black Satin","Velvet", "Satin", "Black Satin","Velvet", "Satin", "Black Satin","Black Satin"],
            "Price": [12.5, 12.5, 10, 12.5, 12.5, 10, 12.5, 12.5, 10, 12.5],
            "Qty Ordered": [60, 1, 2, 5, 7, 20, 40, 20, 10, 2],
        }
    )
    return test_csv.to_csv(index=False).encode()

#Big file 1 byte over 5Mb
big_file = b"x" * (5 * 1024 * 1024 + 1)

# .txt file for wrong content type
json_file = json.dumps('{"hello": "i", "am": "the", "wrong": "file", "file": "type"}').encode("utf-8")