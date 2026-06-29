from collections import defaultdict
import os
from time import monotonic

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import get_password_hash, verify_password
from app.db.database import get_db
from app.schemas.users_schema import TokenResponse, UserResponse, UserCreate, UserLogin
from app.models.users_model import User
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

LOGIN_RATE_LIMIT = 10
LOGIN_RATE_WINDOW_SECONDS = 60
LOGIN_BLOCK_SECONDS = 60
LOGIN_ATTEMPTS = defaultdict(list)
LOGIN_BLOCKED_UNTIL = {}


def is_public_registration_allowed():
    return os.getenv("ALLOW_PUBLIC_REGISTRATION", "true").lower() == "true"


def check_login_rate_limit(client_ip: str):
    now = monotonic()

    blocked_until = LOGIN_BLOCKED_UNTIL.get(client_ip)
    if blocked_until is not None:
        if blocked_until > now:
            raise HTTPException(
                status_code=429,
                detail="Demasiados intentos de login. Intentalo de nuevo en un minuto",
            )
        del LOGIN_BLOCKED_UNTIL[client_ip]

    window_start = now - LOGIN_RATE_WINDOW_SECONDS

    recent_attempts = [
        attempt_time
        for attempt_time in LOGIN_ATTEMPTS[client_ip]
        if attempt_time >= window_start
    ]

    if len(recent_attempts) >= LOGIN_RATE_LIMIT:
        LOGIN_ATTEMPTS[client_ip] = []
        LOGIN_BLOCKED_UNTIL[client_ip] = now + LOGIN_BLOCK_SECONDS
        raise HTTPException(
            status_code=429,
            detail="Demasiados intentos de login. Intentalo de nuevo en un minuto",
        )

    recent_attempts.append(now)
    LOGIN_ATTEMPTS[client_ip] = recent_attempts


@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    if not is_public_registration_allowed():
        raise HTTPException(
            status_code=403,
            detail="El registro publico esta deshabilitado en esta demo",
        )

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
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    client_ip = request.client.host if request.client else "unknown"
    check_login_rate_limit(client_ip)

    existing_user = db.query(User).filter(User.email == form_data.username).first()

    if existing_user is None:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    if verify_password(form_data.password, existing_user.hashed_password) == False:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    data = {"sub": existing_user.email}
    token = TokenResponse(access_token=create_access_token(data), token_type="bearer")

    return token
