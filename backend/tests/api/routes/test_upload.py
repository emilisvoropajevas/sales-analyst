from fastapi.testclient import TestClient

from app.core.config import settings
from tests.utils.seed_upload_data import valid_csv, big_file, json_file

def test_upload_size_over_limit(client: TestClient, superuser_token_headers: dict[str,str]) -> dict:
    r = client.post(f"{settings.API_V1_STR}/upload", headers=superuser_token_headers, files={"file": ("test_file.csv", big_file,"text/csv")})
    assert r.status_code == 413
    results = r.json()
    assert results["detail"] == "Filesize too large, must be below 5.0Mb"

def test_upload_wrong_file_type(client: TestClient, superuser_token_headers: dict[str,str]) -> dict:
    r = client.post(f"{settings.API_V1_STR}/upload", headers=superuser_token_headers, files={"file": ("wrong_file_type", json_file, "application/json")})
    assert r.status_code == 415
    results = r.json()
    assert results["detail"] == "File must be CSV"
    
def test_upload(client: TestClient, superuser_token_headers: dict[str,str]) -> dict:
    r = client.post(f"{settings.API_V1_STR}/upload", headers=superuser_token_headers, files={"file": ("test_file_1", valid_csv(),"text/csv")})
    assert r.status_code == 200
    results = r.json()
    #From seed data - 10 columns inserted
    assert results == {'inserted_rows': 10}
    r_get_uploaded = client.get(f"{settings.API_V1_STR}/orders", headers=superuser_token_headers, params={"model_range": "GHY/0LM8"})
    r_get_results = r_get_uploaded.json()
    assert r_get_uploaded.status_code == 200
    assert len(r_get_results) == 10