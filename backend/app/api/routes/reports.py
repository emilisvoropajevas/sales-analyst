from fastapi import APIRouter
from fastapi import HTTPException

from app.api.deps import CurrentUser, SessionDep
from app.schemas import ReportPublic, ReportPublicWithData, CreateReport
from app.crud import create_report, get_reports, get_report_by_id, delete_report

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/", response_model=ReportPublicWithData)
def add_report(*, session: SessionDep, current_user: CurrentUser, report_in: CreateReport) -> ReportPublicWithData:
    report = create_report(session=session, report_in=report_in)
    return report

@router.get("/", response_model=list[ReportPublic])
def read_reports(*, session: SessionDep, current_user: CurrentUser) -> list[ReportPublic]:
    read_reports_all = get_reports(session=session)
    return read_reports_all

@router.get("/{report_id}", response_model=ReportPublicWithData)
def get_report_id(*, session: SessionDep, current_user: CurrentUser, report_id: int) -> ReportPublicWithData:
    get_report = get_report_by_id(session=session, report_id=report_id)
    if not get_report:
        raise HTTPException(status_code=404, detail="Report not Found")
    return get_report

@router.delete("/{report_id}")
def remove_report(*, session: SessionDep, current_user: CurrentUser, report_id: int) -> dict:
    deleted = delete_report(session=session, report_id=report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"message": "Report deleted"}
    