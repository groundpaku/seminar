
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from db import SessionLocal
from schemas.schema_login import RequestLogin, ResponseLogin
from models.m010_student import M010_student


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30

router = APIRouter(prefix="/login", tags=["login"])


''' DB接続 '''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

''' トーク生成 '''
def create_token_by_id(student_id: int):

    expire = datetime.utcnow() + timedelta(
        minutes=EXPIRE_MINUTES
    )

    payload = {
        "sub": str(student_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

''' トーク生成 '''
def create_token_by_name(name: str):

    expire = datetime.utcnow() + timedelta(
        minutes=EXPIRE_MINUTES
    )

    payload = {
        "sub": name,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

@router.post("/login_id", response_model=ResponseLogin)
def loginId(data: RequestLogin, db: Session = Depends(get_db)):
    try:
        # アカウント検索
        stmt = (
            select(M010_student)
            .where(and_(M010_student.student_id == data.student_id,
                        M010_student.delete_flg == "0"
                ))
            )
        m010_record = db.execute(stmt).scalar_one_or_none()
        if m010_record is not None:
            # パスワード照合
            if not pwd_context.verify(
                data.password,
                m010_record.password_hash
            ):
                return ResponseLogin(result=False,
                                     message="Password mismatch.",
                                     token="")
            else:
                # トークン生成
                token = create_token_by_id(m010_record.student_id)
                return ResponseLogin(result=True,
                                     message="",
                                     token=token)
        else:
            return ResponseLogin(result=False, 
                                 message="Student does not exist.",
                                 token="")
    except Exception as e:
        return ResponseLogin(result=False, 
                             message=(str(e)),
                             token="")

@router.post("/login_name", response_model=ResponseLogin)
def loginName(data: RequestLogin, db: Session = Depends(get_db)):
    try:
        # アカウント検索
        stmt = (
            select(M010_student)
            .where(and_(M010_student.student_id == data.student_id,
                        M010_student.delete_flg == "0"
                ))
            )
        m010_record = db.execute(stmt).scalar_one_or_none()
        if m010_record is not None:
            # パスワード照合
            if not pwd_context.verify(
                data.password,
                m010_record.password_hash
            ):
                return ResponseLogin(result=False,
                                     message="Password mismatch.",
                                     token="")
            else:
                # トークン生成
                token = create_token_by_name(m010_record.name)
                return ResponseLogin(result=True,
                                     message="",
                                     token=token)
        else:
            return ResponseLogin(result=False, 
                                 message="Student does not exist.",
                                 token="")
    except Exception as e:
        return ResponseLogin(result=False, 
                             message=(str(e)),
                             token="")