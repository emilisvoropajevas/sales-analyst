from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, Reports
from app.schemas import CreateReport

def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def get_user_by_username(*, session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    session_user = session.exec(statement).first()
    return session_user

# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"

def authenticate(*, session: Session, username: str, password: str) -> User | None:
    db_user = get_user_by_username(session=session, username=username)
    if not db_user:
        # Prevent timing attacks by running password verification even when user doesn't exist
        # This ensures the response time is similar whether or not the email exists
        verify_password(password, DUMMY_HASH)
        return None
    verified, updated_password_hash = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    if updated_password_hash:
        db_user.hashed_password = updated_password_hash
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user
    
def create_report(*, session: Session, report_in: CreateReport) -> Reports:
    db_report = Reports.model_validate(report_in)
    session.add(db_report)
    session.commit()
    session.refresh(db_report)
    return db_report

def get_reports(*, session: Session) -> list[Reports]:
    statement = select(Reports)
    return session.exec(statement).all()

def get_report_by_id(*, session: Session, report_id: int) -> Reports | None:
    statement = select(Reports).where(Reports.id == report_id)
    return session.exec(statement).first()

def delete_report(*, session: Session, report_id: int) -> bool:
    statement = select(Reports).where(Reports.id == report_id)
    report = session.exec(statement).first()
    if not report:
        return False
    session.delete(report)
    session.commit()
    return True