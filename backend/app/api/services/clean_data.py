import pandas as pd
from io import BytesIO

required_columns = ['Order Date', 'Order ID', 'Product SKU', 'Product Name', 'Qty Ordered', 'Price']

def clean_and_format_csv(csv_file):

    try:
        uploaded_file_as_dataframe = pd.read_csv(BytesIO(csv_file))
    except Exception:
        raise ValueError("Could not parse CSV file")
    if uploaded_file_as_dataframe.empty:
        raise ValueError("CSV file is empty")
    
    missing_columns = set(required_columns) - set(uploaded_file_as_dataframe.columns)
    if missing_columns:
        raise ValueError(f"Column {missing_columns} missing from data")
    
    uploaded_file_as_dataframe['Order Date'] = (pd.to_datetime(uploaded_file_as_dataframe['Order Date'], errors = 'coerce')).dt.normalize()

    if uploaded_file_as_dataframe['Order Date'].isnull().sum() / len(uploaded_file_as_dataframe['Order Date']) > 0.1:
        raise ValueError("Too many null dates")
    else:
        uploaded_file_as_dataframe['Order Date'].dropna()

    report_dataframe = uploaded_file_as_dataframe[['Order Date', 'Order ID', 'Product SKU', 'Product Name', 'Qty Ordered', 'Price']].copy()
    
    report_dataframe = report_dataframe[report_dataframe['Product SKU'].str.contains("-f", na = False)]

    report_dataframe = report_dataframe.sort_values(by = 'Order Date', ascending= True).reset_index(drop = True)

    report_dataframe['Model Range'] = report_dataframe['Product SKU'].str.rsplit("/", n=1).str[0]

    report_dataframe = report_dataframe.rename(columns={
        "Order Date": "order_date",
        "Order ID": "order_id",
        "Product SKU": "product_sku",
        "Product Name": "product_name",
        "Qty Ordered": "qty_ordered",
        "Price": "price",
        "Model Range": "model_range"

    })

    return report_dataframe.to_dict(orient="records")
