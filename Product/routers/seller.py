from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import login as SellerSchema
from ..models import Seller

router = APIRouter()
# for sellers we can create similar endpoints for CRUD operations as we did for products.
@router.post("/sellers",tags=["Sellers"])
def create_seller(seller: SellerSchema, db: Session = Depends(get_db)):
    db_seller = Seller(name=seller.name, email=seller.email, password=seller.password)
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return {"message": "Seller created successfully", "seller": SellerSchema.from_orm(db_seller)}