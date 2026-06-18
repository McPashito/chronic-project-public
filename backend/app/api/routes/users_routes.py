from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from app.db.database import get_db


from app.schemas.users_schema import (
    UserResponse,
    UserEdit,
    ChangePassword,
    TokenResponse,
)
from app.models.users_model import User
from app.core.security import get_current_user, verify_password, get_password_hash
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def authenticated_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/edit_user", response_model=UserResponse)
def edit_user(
    user_put: UserEdit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_info = db.query(User).filter(User.id == current_user.id).first()
    if user_info is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user_info.name = user_put.name
    user_info.surname = user_put.surname
    user_info.date_of_birth = user_put.date_of_birth
    user_info.subscription_type = user_put.subscription_type

    db.commit()
    db.refresh(user_info)

    return user_info


@router.put("/change_password")
def change_password(
    password_data: ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_change = db.query(User).filter(User.id == current_user.id).first()
    if user_change is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    password_ok = verify_password(
        password_data.old_password, user_change.hashed_password
    )

    if not password_ok:
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    user_change.hashed_password = get_password_hash(password_data.new_password)

    db.commit()
    db.refresh(user_change)

    return {"message": "Contraseña actualizada correctamente"}
