"""Authentication routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..db import get_db
from ..logging_utils import append_log
from ..models import User
from ..security import create_access_token, hash_password, verify_password

router = APIRouter()


@router.post("/signup", response_model=schemas.Message)
def signup(payload: schemas.SignupRequest, db: Session = Depends(get_db)) -> schemas.Message:
    """Create a new user account."""

    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User exists")
    user = User(email=payload.email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    append_log("signup", user=user.email, path="/auth/signup", status="ok")
    return schemas.Message(message="signup successful")


@router.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)) -> schemas.TokenResponse:
    """Authenticate and return a JWT."""

    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        append_log("login_failed", user=payload.email, path="/auth/login", status="denied")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(user_id=user.id, role=user.role)
    append_log("login", user=user.email, path="/auth/login", status="ok")
    return schemas.TokenResponse(token=token)
