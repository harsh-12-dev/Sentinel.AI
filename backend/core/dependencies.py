from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import User
from backend.core.security import decode_access_token

security_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Token se logged-in user nikalta hai. Galat token par 401."""

    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Token decode karo
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise credentials_error

    # 2. Token se user id nikalo ("sub" me daali thi login ke time)
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_error

    # 3. Us id ka user database me abhi bhi hai?
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_error

    return user