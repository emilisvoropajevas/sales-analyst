from fastapi import APIRouter

from app.api.routes import login, upload, orders
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(upload.router)
api_router.include_router(orders.router)

#Check models and validate schemas, 

#Go through create user, im only using one user so requires some refactoring

#Write testing files for each endpoint

#Test in localhost for successfull data creation and filtering based on columns, adjust if need be

#Migrate to alembic for database migrations

#bash scripts for checking database running before running alembic migrations

# check understanding of each file and reason for existing 

#frontend setup 