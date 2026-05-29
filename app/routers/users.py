from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.users import User
from app.schemas.users import UserResponse, UserUpdate
from app.core.security import hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_me(updated: UserUpdate, current_user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    if updated.username:
        current_user.username = updated.username
    if updated.email:
        current_user.email = updated.email
    if updated.password:
        current_user.hashed_password = hash_password(updated.password)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()

