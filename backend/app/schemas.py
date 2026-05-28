import uuid
from datetime import datetime
from sqlmodel import SQLModel

class OrdersPublic(SQLModel):
    order_id: int
    order_date: datetime
    product_sku: str
    product_name: str
    price: float
    qty_ordered: float
    model_range : str

class CreateReport(SQLModel):
    name: str
    date_range_start: datetime
    date_range_end: datetime
    sku: str | None = None
    model_range: str

class ReportPublic(SQLModel):
    id: int
    name: str
    created_at: datetime
    date_range_start: datetime
    date_range_end: datetime
    sku: str | None = None
    model_range: str

class ReportPublicWithData(ReportPublic):
    data: list[OrdersPublic]

class UserCreate(SQLModel):
    username: str
    password: str

class UserPublic(SQLModel):
    id: uuid.UUID
    username: str
    is_active: bool
    is_superuser: bool

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(SQLModel):
    sub: str | None = None

#Note to self - I changed the sku field to product sku