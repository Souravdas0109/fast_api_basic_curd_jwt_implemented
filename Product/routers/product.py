from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Product as ProductSchema
from ..models import Product, Seller
from ..auth import get_current_seller

router = APIRouter()

@router.post("/products",tags=["Products"])
def create_product(product: ProductSchema, db: Session = Depends(get_db), current_seller: Seller = Depends(get_current_seller)):
    if current_seller is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    db_product = Product(name=product.name, description=product.description, price=product.price, seller_id=current_seller.id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"message": "Product created successfully", "product": ProductSchema.from_orm(db_product)}

@router.get("/products",tags=["Products"])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.get("/products/{product_id}",tags=["Products"])
def read_product(product_id: int, db: Session = Depends(get_db)):
    product=db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        return {"message": "Product not found"}
    return product

@router.put("/products/{product_id}",tags=["Products"])
def update_product(product_id: int, product: ProductSchema, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        return {"message": "Product not found"}
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db.commit()
    return {"message": "Product updated successfully", "product": ProductSchema.from_orm(db_product)}

@router.delete("/products/{product_id}",tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        return {"message": "Product not found"}
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}