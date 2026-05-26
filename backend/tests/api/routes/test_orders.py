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

"""
what happens if date range does not exist? 
end_date without start_date
both dates -> should show correct range
sku -> should show correct sku products
model_range -> returns match
date_range that has no matching records -> should return empty list

@router.get("/", response_model=list[Orders])
def get_orders(session: SessionDep, current_user: CurrentUser, 
               start_date: datetime | None = None, end_date: datetime | None = None, 
               model_range: str | None = None, sku: str | None = None) -> list[Orders]:
    
    if (start_date and not end_date) or (end_date and not start_date):
        raise HTTPException(status_code=400, detail="Missing start or end date")
    result = read_orders(session=session, start_date=start_date, end_date=end_date, model_range=model_range, sku=sku)
    return result

test the if statement assert responses
test return values from raw_test_data
"""