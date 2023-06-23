"""User routes."""
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    create_user,
    get_current_active_user,
    Token,
    User,
)

router = APIRouter(
    prefix="/users/me",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    """Get current user.

    Parameters
    ----------
    current_user
        Current user

    Returns
    -------
    User
        Current user
    """
    return current_user


@router.get("/items/")
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]) -> list[dict[str, str]]:
    """Get current user's items.

    Parameters
    ----------
    current_user
        Current user

    Returns
    -------
    list[dict[str, str]]
        Current user's items
    """
    return [{"owner": current_user.username}]


@router.get("/signup")
async def signup(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict[str, str]:
    """Signup."""
    username = form_data.username
    password = form_data.password
    user = authenticate_user(username, password)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )
    user = create_user(username, password, form_data.email, form_data.full_name)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Error creating user",
        )
    return {"message": "User created"}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict[str, str]:
    """Login for access token.

    Parameters
    ----------
    form_data
        Form data

    Returns
    -------
    dict[str, str]
        Access token

    Raises
    ------
    HTTPException
        Incorrect username or password
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
