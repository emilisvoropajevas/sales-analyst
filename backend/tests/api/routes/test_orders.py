from fastapi.testclient import TestClient
from datetime import datetime

from app.models import Orders
from app.core.config import settings

def test_orders_default_empty_fields(client: TestClient, superuser_token_headers: dict[str,str]) -> list[Orders]:
    required_columns = ["id", "order_id", "order_date", "product_sku", "product_name", "price", "qty_ordered", "model_range"]
    r = client.get(f"{settings.API_V1_STR}/orders", headers=superuser_token_headers)
    results = r.json()

    assert r.status_code == 200
    for column in required_columns:
        assert column in results[0] 
    
def test_orders_no_startdate(client: TestClient, superuser_token_headers: dict[str,str]) -> list[Orders]:
    r = client.get(f"{settings.API_V1_STR}/orders", headers=superuser_token_headers, params={"start_date": datetime(2026, 5, 10, 18, 59)})
    assert r.status_code == 400

def test_orders_no_enddate(client: TestClient, superuser_token_headers: dict[str,str]) -> list[Orders]:
    r = client.get(f"{settings.API_V1_STR}/orders", headers=superuser_token_headers, params={"end_date": datetime(2026, 5, 15, 8, 21)})
    assert r.status_code == 400

def test_orders_date_range(client: TestClient, superuser_token_headers: dict[str,str])-> list[Orders]:
    r = client.get(f"{settings.API_V1_STR}/orders", headers=superuser_token_headers, params={"start_date": datetime(2026, 5, 15, 1, 12), "end_date": datetime(2026, 5, 20, 16, 19)})
    assert r.status_code == 200
    results = r.json()
    #from seed data, this should only show 5 records
    assert len(results) == 5

def test_orders_out_of_bounds_date(client: TestClient, superuser_token_headers: dict[str,str]) -> list[Orders]:
    r = client.get(f"{settings.API_V1_STR}/orders", headers=superuser_token_headers, params={"start_date": datetime(2026, 6, 20, 16, 19), "end_date": datetime(2026, 7, 20, 16, 19)})
    assert r.status_code == 200
    results = r.json()
    assert results == []

def test_orders_sku_range(client: TestClient, superuser_token_headers: dict[str,str]) -> list[Orders]:
    r = client.get(f"{settings.API_V1_STR}/orders", headers=superuser_token_headers, params={"sku": "DWP/1935/01"})
    assert r.status_code == 200
    results = r.json()
    for sku in results:
        assert sku["product_sku"] == "DWP/1935/01"

def test_orders_sku_model_range(client: TestClient, superuser_token_headers: dict[str,str]) -> list[Orders]:
    r = client.get(f"{settings.API_V1_STR}/orders", headers=superuser_token_headers, params={"model_range": "DWP/1935"})
    assert r.status_code == 200
    results = r.json()
    for model in results:
        assert model["model_range"] == "DWP/1935"

#Bad sku? Bad model range? - returns error