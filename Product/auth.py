from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database import get_db
from .models import Seller

# NOTE: Replace this secret with a secure value from env/config in production.
SECRET_KEY = "change-me-to-a-random-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# werkzeug's PBKDF2-SHA256 avoids bcrypt 72-byte limitations
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return check_password_hash(hashed_password, plain_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    return generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)


def authenticate_seller(db: Session, email: str, password: str) -> Optional[Seller]:
    seller = db.query(Seller).filter(Seller.email == email).first()
    if not seller:
        return None

    # If stored password is hashed, check_password_hash will return True.
    if verify_password(password, seller.password):
        return seller

    # Fallback: if the stored value is plain-text, compare directly and
    # re-hash and persist on successful match.
    if seller.password == password:
        seller.password = get_password_hash(password)
        db.add(seller)
        db.commit()
        db.refresh(seller)
        return seller

    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_seller(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Seller:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        seller_id: str = payload.get("sub")
        if seller_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    seller = db.query(Seller).filter(Seller.id == int(seller_id)).first()
    if seller is None:
        raise credentials_exception
    return seller
