from fastapi.testclient import TestClient
from datetime import datetime

from app.schemas import ReportPublic, ReportPublicWithData
from app.core.config import settings


def test_add_report(client: TestClient, superuser_token_headers: dict[str, str]) -> ReportPublic:
    data = {
        "name": "test_report",
        "date_range_start": datetime(2026, 5, 10, 18, 59).isoformat(),
        "date_range_end": datetime(2026, 5, 20, 16, 19).isoformat(),
        "sku": "DWP/1935/01",
        "model_range": "DWP/1935",
    }
    r = client.post(f"{settings.API_V1_STR}/reports", headers=superuser_token_headers, json=data)
    assert r.status_code == 200
    results = r.json()
    required_column_names = ["id", "name", "created_at", "date_range_start", "date_range_end", "sku", "model_range"]

    for column in required_column_names:
        assert column in results
    
    for name, item in data.items():
        assert name in results
        assert item == results[name]


def test_add_report_missing_model_range(client: TestClient, superuser_token_headers: dict[str,str]) -> ReportPublic:
    data = {
        "name": "test_report",
        "date_range_start": datetime(2026, 5, 10, 18, 59).isoformat(),
        "date_range_end": datetime(2026, 5, 20, 16, 19).isoformat(),
        "sku": "DWP/1935/01",
    }
    r = client.post(f"{settings.API_V1_STR}/reports", headers=superuser_token_headers, json=data)
    assert r.status_code == 422


def test_add_report_empty_name(client: TestClient, superuser_token_headers: dict[str,str]) -> ReportPublic:
    data = {
        "name": " ",
        "date_range_start": datetime(2026, 5, 10, 18, 59).isoformat(),
        "date_range_end": datetime(2026, 5, 20, 16, 19).isoformat(),
        "sku": "DWP/1935/01",
        "model_range": "DWP/1935",
    }
    r = client.post(f"{settings.API_V1_STR}/reports", headers=superuser_token_headers, json=data)
    results = r.json()
    assert r.status_code == 422
    assert results["detail"] == "Cannot be empty"


def test_add_report_empty_sku(client: TestClient, superuser_token_headers: dict[str,str]) -> ReportPublic:
    data = {
        "name": "test_report",
        "date_range_start": datetime(2026, 5, 10, 18, 59).isoformat(),
        "date_range_end": datetime(2026, 5, 20, 16, 19).isoformat(),
        "sku": " ",
        "model_range": "DWP/1935",
    }
    r = client.post(f"{settings.API_V1_STR}/reports", headers=superuser_token_headers, json=data)
    results = r.json()
    assert r.status_code == 422
    assert results["detail"] == "Cannot be empty"


def test_add_report_empty_model_range(client: TestClient, superuser_token_headers: dict[str,str]) -> ReportPublic:
    data = {
        "name": "test_report",
        "date_range_start": datetime(2026, 5, 10, 18, 59).isoformat(),
        "date_range_end": datetime(2026, 5, 20, 16, 19).isoformat(),
        "sku": "DWP/1935/01",
        "model_range": " ",
    }
    r = client.post(f"{settings.API_V1_STR}/reports", headers=superuser_token_headers, json=data)
    results = r.json()
    assert r.status_code == 422
    assert results["detail"] == "Cannot be empty"


def test_read_reports(client: TestClient, superuser_token_headers: dict[str,str]) -> list[ReportPublic]:
    r = client.get(f"{settings.API_V1_STR}/reports", headers=superuser_token_headers)
    assert r.status_code == 200
    results = r.json()
    assert len(results) == 1
    assert "test_report" == results[0]["name"]


def test_get_report_by_id(client: TestClient, superuser_token_headers: dict[str,str]) -> ReportPublicWithData:
    #Create new report
    data = {
        "name": "test_report",
        "date_range_start": datetime(2026, 5, 10, 18, 59).isoformat(),
        "date_range_end": datetime(2026, 5, 20, 16, 19).isoformat(),
        "sku": "DWP/1935/01",
        "model_range": "DWP/1935",
    }
    r_id = client.post(f"{settings.API_V1_STR}/reports", headers=superuser_token_headers, json=data)
    report_id = r_id.json()["id"]
    r = client.get(f"{settings.API_V1_STR}/reports/{report_id}", headers=superuser_token_headers)
    assert r.status_code == 200
    results = r.json()
    additional_columns = ["order_id", "order_date", "product_sku", "product_name", "price", "qty_ordered", "model_range"]
    for column in additional_columns:
        assert column in results["data"][0]

# What if report does not exist?
def test_get_report_by_id_no_report(client: TestClient, superuser_token_headers: dict[str,str]) -> ReportPublicWithData:
    r = client.get(f"{settings.API_V1_STR}/reports/{10}", headers=superuser_token_headers)
    assert r.status_code == 404
    results = r.json()
    assert results["detail"] == "Report not found"


def test_remove_report(client: TestClient, superuser_token_headers: dict[str,str]) -> dict:
    data = {
        "name": "test_report",
        "date_range_start": datetime(2026, 5, 10, 18, 59).isoformat(),
        "date_range_end": datetime(2026, 5, 20, 16, 19).isoformat(),
        "sku": "DWP/1935/01",
        "model_range": "DWP/1935",
    }
    r_id = client.post(f"{settings.API_V1_STR}/reports", headers=superuser_token_headers, json=data)
    report_id = r_id.json()["id"]
    r = client.delete(f"{settings.API_V1_STR}/reports/{report_id}", headers=superuser_token_headers)
    assert r.status_code == 200
    results = r.json()
    assert results["message"] == "Report deleted"
    r_deleted_report = client.get(f"{settings.API_V1_STR}/reports/{report_id}", headers=superuser_token_headers)
    assert r_deleted_report.status_code == 404
    deleted_results = r_deleted_report.json()
    assert deleted_results["detail"] == "Report not found"