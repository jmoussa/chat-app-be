import logging
from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from requests import RegisterRequest

from controllers import (
    create_user,
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from mongodb import get_nosql_db, AsyncIOMotorClient
from models import Token
from config import MONGODB_DB_NAME

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/token", tags=["Authentication"], response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncIOMotorClient = Depends(get_nosql_db)
):
    """
    Login
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/register", tags=["Authentication"])
async def create_user_in_db(request: RegisterRequest, client: AsyncIOMotorClient = Depends(get_nosql_db)):
    db = client[MONGODB_DB_NAME]
    collection = db.users
    try:
        await create_user(request, collection)
    except Exception:
        logger.error("REGISTER: User already in db, logging in")
        pass

    logger.info(f"{request.username}\n{request.password}")
    # now login and generate token
    user = await authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
