from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import Seller as SellerSchema, login as LoginSchema
from ..models import Seller
from ..database import get_db
from ..auth import authenticate_seller, create_access_token, get_current_seller
from datetime import timedelta

router = APIRouter()


@router.post("/login/token", tags=["Authentication"])
def login_for_access_token(login: LoginSchema, db: Session = Depends(get_db)):
    seller = authenticate_seller(db, login.email, login.password)
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": str(seller.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", tags=["Authentication"])
def read_current_seller(current_seller: Seller = Depends(get_current_seller)):
    return SellerSchema.from_orm(current_seller)
