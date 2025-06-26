from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from database import AsyncSession
from dependencies import get_db_session
from member.schemas import LoginResponse
from auth.service import authenticate

router = APIRouter(prefix="/v1", tags=["auth"])


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    oauth2_request: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    raise NameError
    token = await authenticate(db_session, oauth2_request.username, oauth2_request.password)
    return JSONResponse(content={"token": token})
