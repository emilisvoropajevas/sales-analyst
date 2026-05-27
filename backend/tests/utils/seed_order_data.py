from datetime import datetime

raw_test_data = {
    "order_id": [
        "442912","443547","441884","447418","441152",
        "441127","442765","440424","443677","443069"
    ],

    "order_date": [
        datetime(2026, 5, 10, 18, 59),
        datetime(2026, 5, 4, 15, 5),
        datetime(2026, 5, 10, 10, 51),
        datetime(2026, 5, 10, 23, 0),
        datetime(2026, 5, 15, 1, 12),
        datetime(2026, 5, 15, 21, 44),
        datetime(2026, 5, 11, 21, 57),
        datetime(2026, 5, 20, 9, 40),
        datetime(2026, 5, 20, 16, 19),
        datetime(2026, 5, 15, 8, 21)
    ],

    "product_sku": [
        "DWP/1935/01","DWP/1935/01","DWP/1935/01",
        "MFP/8926/01","DWP/1865/05","DWP/1935/01",
        "DWP/1935/01","CBT/0984/01","BFW/GI0989/01",
        "DWP/1935/01"
    ],

    "product_name": [
        "Product1","Product1","Product1","Product1","Product1",
        "Product1","Product1","Product1","Product1","Product1"
    ],

    "price": [
        10.1, 11.2, 10.1, 11.2, 10.1,
        11.2, 10.1, 11.2, 10.1, 11.2
    ],

    "qty_ordered": [
        43, 7, 56, 58, 105,
        99, 46, 105, 21, 34
    ],

    "model_range": [
        "DWP/1935","DWP/1935","DWP/1935","DWP/1935","DWP/1935",
        "DWP/1935","DWP/1935","DWP/1935","DWP/1935","DWP/1935"
    ]
}