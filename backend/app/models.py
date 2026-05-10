import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)

class Orders(SQLModel, table=True):
    id : int | None = Field(default=None, primary_key=True)
    order_id: int
    order_date: datetime = Field(index=True)
    product_sku: str
    product_name: str
    price: float
    qty_ordered: float
    model_range : str
    #Can have multiple order id with the same items, need to check all fields to find duplicates
    __table_args__ = (
        UniqueConstraint("order_id", "product_sku", "order_date", "qty_ordered", "price", "model_range"),
    )

class Reports(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=get_datetime_utc, sa_type=DateTime(timezone=True),)
    date_range_start: datetime
    date_range_end: datetime
    data: dict = Field(sa_column=Column(JSONB))

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime | None = Field(default_factory=get_datetime_utc, sa_type=DateTime(timezone=True),)
    is_superuser: bool = False
    is_active: bool = True

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
