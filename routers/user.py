from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, Path, HTTPException, APIRouter
from ..database import SessionLocal
from .auth import get_current_user
from starlette import status
from ..models import Todos, Users
from pydantic import BaseModel, Field
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserRequest(BaseModel):

    password: str
    new_password: str = Field(min_lenght=3, max_lenght=250)

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependency, db: db_dependency):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/password/', status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: user_dependency, db: db_dependency, user_request: UserRequest ):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_request.password, user_model.hashed_pass):
        raise HTTPException(status_code=401, detail='Error on password change')

    user_model.hashed_pass = bcrypt_context.hash(user_request.new_password)

    db.add(user_model)
    db.commit()

@router.put('/phone/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def update_phone(user: user_dependency, db: db_dependency, phone_number: str):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.phone_number = phone_number

    db.add(user_model)
    db.commit()