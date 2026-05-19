from typing import Any
from datetime import datetime

from fastapi import APIRouter
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import Orders

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=list[Orders])
def get_orders(
    session: SessionDep, 
    current_user: CurrentUser, 
    start_date: datetime, 
    end_date: datetime, 
    model_range: str | None = None, 
    sku: str | None = None
) -> Any:
    
    statement = select(Orders).where(
        Orders.order_date >= start_date,
        Orders.order_date <= end_date,
    )

    if model_range:
        statement = statement.where(Orders.model_range == model_range)
    
    if sku:
        statement = statement.where(Orders.product_sku == sku)
    
    results = session.exec(statement).all()

    return results

#migrate to crud (all db interactions in one file)