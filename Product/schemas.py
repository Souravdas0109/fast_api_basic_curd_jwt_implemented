from pydantic import BaseModel, ConfigDict

class Product(BaseModel):
    name: str
    description: str
    price: float
    seller_id: int
    model_config = ConfigDict(from_attributes=True)

class Seller(BaseModel):
    name: str
    email: str
    password: str
    model_config = ConfigDict(from_attributes=True)

class login(BaseModel):
    email: str
    password: str