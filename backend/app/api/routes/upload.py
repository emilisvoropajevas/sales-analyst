from fastapi import UploadFile, APIRouter, HTTPException
from sqlalchemy.dialects.postgresql import insert

from app.api.services.clean_data import clean_and_format_csv
from app.api.deps import SessionDep, CurrentUser
from app.models import Orders

router = APIRouter()

MAX_FILE_SIZE = 5 * 1024 * 1024

@router.post("/reports/upload")
async def upload_to_database(
    file: UploadFile,
    session: SessionDep,
    current_user: CurrentUser,
    ):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"Filesize too large, must be below {MAX_FILE_SIZE/(1024*1024)} Mb")
    if file.content_type != "text/csv":
        raise HTTPException(status_code=415, detail="File must be CSV")
    
    contents = await file.read()
    try:
        rows = clean_and_format_csv(contents)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    statement = insert(Orders).values(rows)
    statement = statement.on_conflict_do_nothing()
    result = session.exec(statement)
    session.commit()
    return {"inserted_rows": result.rowcount}