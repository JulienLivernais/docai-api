from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.repositories.users import (
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    get_user_by_username,
    delete_user
)
from app.schemas.users import UserResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserResponse])
def list_all_users(
        db: Session = Depends(get_db),
        current_admin=Depends(get_current_admin)
):
    return get_all_users(db)


@router.get("/users/by-email", response_model=UserResponse)
def find_by_email(
        email: str,
        db: Session = Depends(get_db),
        current_admin=Depends(get_current_admin)
):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/users/by-username", response_model=UserResponse)
def find_by_username(
        username: str,
        db: Session = Depends(get_db),
        current_admin=Depends(get_current_admin)
):
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/users/{user_id}", response_model=UserResponse)
def find_by_id(
        user_id: int,
        db: Session = Depends(get_db),
        current_admin=Depends(get_current_admin)
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_admin=Depends(get_current_admin)
):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

