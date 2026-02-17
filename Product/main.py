from fastapi import FastAPI
from .database import Base, engine
from .routers import product, seller, login

app = FastAPI(
    title="Product API",
    description="API for managing products and sellers",
    contact={
        "name": "Sourav",
    }
)

Base.metadata.create_all(bind=engine)

app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)
