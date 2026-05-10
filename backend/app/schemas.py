from datetime import datetime
from sqlmodel import SQLModel

class CreateReport(SQLModel):
    name: str
    date_range_start: datetime
    date_range_end: datetime
    data: list[dict]

class ReportPublic(SQLModel):
    id: int
    name: str
    created_at: datetime
    date_range_start: datetime
    date_range_end: datetime

class ReportPublicWithData(ReportPublic):
    data: dict