from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import get_password_hash, verify_password
from app.db.database import get_db
from app.schemas.users_schema import TokenResponse, UserResponse, UserCreate, UserLogin
from app.models.users_model import User
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        name=user.name,
        surname=user.surname,
        date_of_birth=user.date_of_birth,
        subscription_type=user.subscription_type or "standard",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=TokenResponse)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == form_data.username).first()

    if existing_user is None:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    if verify_password(form_data.password, existing_user.hashed_password) == False:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    data = {"sub": existing_user.email}
    token = TokenResponse(access_token=create_access_token(data), token_type="bearer")

    return token
