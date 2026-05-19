from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.crud import read_orders
from app.api.deps import CurrentUser, SessionDep
from app.models import Orders

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=list[Orders])
def get_orders(session: SessionDep, current_user: CurrentUser, 
               start_date: datetime | None = None, end_date: datetime | None = None, 
               model_range: str | None = None, sku: str | None = None) -> list[Orders]:
    
    if (start_date and not end_date) or (end_date and not start_date):
        raise HTTPException(status_code=400, detail="Missing start or end date")
    result = read_orders(session=session, start_date=start_date, end_date=end_date, model_range=model_range, sku=sku)
    return result