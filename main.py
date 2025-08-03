from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional

import dal
from database import init_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

# Pydantic models for request/response
class CategoryModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class CategoryCreate(BaseModel):
    name: str = Field(..., example="Electronics")

class ProductModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category_id: int

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str = Field(..., example="Smartphone")
    description: Optional[str] = Field(None, example="Android phone 128GB")
    price: float = Field(..., gt=0)
    category_id: int

# --- CATEGORIES ---
@app.post("/categories/", response_model=CategoryModel)
async def add_category(category: CategoryCreate):
    cat = await dal.create_category(category.name)
    return cat.as_dict()

@app.get("/categories/", response_model=List[CategoryModel])
async def list_categories():
    cats = await dal.get_categories()
    return [c.as_dict() for c in cats]

@app.get("/categories/{category_id}", response_model=CategoryModel)
async def get_category(category_id: int):
    cat = await dal.get_category_by_id(category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat.as_dict()

# --- PRODUCTS ---
@app.post("/products/", response_model=ProductModel)
async def add_product(product: ProductCreate):
    # Ensure category exists
    cat = await dal.get_category_by_id(product.category_id)
    if not cat:
        raise HTTPException(status_code=400, detail="Category not found")
    prod = await dal.create_product(product.name, product.description, product.price, product.category_id)
    return prod.as_dict()

@app.get("/products/", response_model=List[ProductModel])
async def list_products():
    prods = await dal.get_products()
    return [p.as_dict() for p in prods]

@app.get("/products/{product_id}", response_model=ProductModel)
async def get_product(product_id: int):
    prod = await dal.get_product_by_id(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod.as_dict()

@app.get("/products/by_category/{category_id}", response_model=List[ProductModel])
async def products_by_category(category_id: int):
    cat = await dal.get_category_by_id(category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    prods = await dal.get_products_by_category(category_id)
    return [p.as_dict() for p in prods]
