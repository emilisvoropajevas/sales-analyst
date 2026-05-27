from fastapi import UploadFile, APIRouter, HTTPException

from app.api.services.clean_data import clean_and_format_csv
from app.crud import upload_orders
from app.api.deps import SessionDep, CurrentUser

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/")
async def upload_to_db(file: UploadFile, session: SessionDep, current_user: CurrentUser) -> dict:
    MAX_FILE_SIZE = 5 * 1024 * 1024
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"Filesize too large, must be below {MAX_FILE_SIZE/(1024*1024)} Mb")
    if file.content_type != "text/csv":
        raise HTTPException(status_code=415, detail="File must be CSV")
    contents = await file.read()
    try:
        rows = clean_and_format_csv(contents)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    uploaded = upload_orders(session=session, orders_in=rows)
    return uploaded