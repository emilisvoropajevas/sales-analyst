from fastapi.testclient import TestClient
import json
from datetime import datetime

from app.schemas import ReportPublic, ReportPublicWithData, CreateReport
from app.core.config import settings

#Test Reports endpoint 
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


"""
class CreateReport(SQLModel):
    name: str
    date_range_start: datetime
    date_range_end: datetime
    sku: str | None = None
    model_range: str


@router.post("/", response_model=ReportPublic)
def add_report(*, session: SessionDep, current_user: CurrentUser, report_in: CreateReport) -> ReportPublic:
    report = create_report(session=session, report_in=report_in)
    return report


@router.get("/", response_model=list[ReportPublic])
def read_reports(*, session: SessionDep, current_user: CurrentUser) -> list[ReportPublic]:
    read_reports_all = get_reports(session=session)
    return read_reports_all

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