from fastapi.testclient import TestClient
from datetime import datetime

from app.schemas import ReportPublic, ReportPublicWithData, CreateReport
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

#Missing model_range - should return 422 (Cannot be empty) - empty sku, empty name

def test_add_report_missing_model_range(client: TestClient, superuser_token_headers: dict[str,str]) -> ReportPublic:
    data = {
        "name": "test_report",
        "date_range_start": datetime(2026, 5, 10, 18, 59).isoformat(),
        "date_range_end": datetime(2026, 5, 20, 16, 19).isoformat(),
        "sku": "DWP/1935/01",
    }
    r = client.post(f"{settings.API_V1_STR}/reports", headers=superuser_token_headers, json=data)
    assert r.status_code == 422



def test_read_reports(client: TestClient, superuser_token_headers: dict[str,str]) -> list[ReportPublic]:
    r = client.get(f"{settings.API_V1_STR}/reports", headers=superuser_token_headers)
    assert r.status_code == 200
    results = r.json()
    assert len(results) == 1
    assert "test_report" == results[0]["name"]


"""
class CreateReport(SQLModel):
    name: str
    date_range_start: datetime
    date_range_end: datetime
    sku: Annotated[str | None, AfterValidator(is_empty)] = None
    model_range: Annotated[str, AfterValidator(is_empty)]

#This needs to query the db and return reportpublic with data (metadata)
@router.get("/{report_id}", response_model=ReportPublicWithData)
def get_report_id(*, session: SessionDep, current_user: CurrentUser, report_id: int) -> ReportPublicWithData:
    get_report = get_report_by_id(session=session, report_id=report_id)
    if not get_report:
        raise HTTPException(status_code=404, detail="Report not Found")
    report = read_orders(session=session, model_range=get_report.model_range, sku=get_report.sku, start_date=get_report.date_range_start, end_date=get_report.date_range_end)
    orders = [OrdersPublic.model_validate(order) for order in report]
    # ** unpacks dictionary into keyword arguments
    return ReportPublicWithData(**get_report.model_dump(), data=orders)

@router.delete("/{report_id}")
def remove_report(*, session: SessionDep, current_user: CurrentUser, report_id: int) -> dict:
    deleted = delete_report(session=session, report_id=report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"message": "Report deleted"}
"""