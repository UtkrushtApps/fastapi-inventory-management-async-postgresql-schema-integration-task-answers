
from typing import List, Optional
import asyncpg
from database import get_pool

class Product:
    def __init__(self, id: int, name: str, description: Optional[str], price: float, category_id: int):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category_id = category_id

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'category_id': self.category_id
        }

class Category:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

async def create_category(name: str) -> Category:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO categories(name)
            VALUES($1)
            RETURNING id, name
            """, name)
        return Category(**dict(row))

async def get_categories() -> List[Category]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name FROM categories ORDER BY name;")
        return [Category(**dict(row)) for row in rows]

async def get_category_by_id(category_id: int) -> Optional[Category]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, name FROM categories WHERE id=$1;", category_id)
        return Category(**dict(row)) if row else None

async def create_product(name: str, description: Optional[str], price: float, category_id: int) -> Product:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO products(name, description, price, category_id)
            VALUES($1, $2, $3, $4)
            RETURNING id, name, description, price, category_id
            """, name, description, price, category_id)
        return Product(**dict(row))

async def get_products() -> List[Product]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, name, description, price, category_id FROM products ORDER BY id;")
        return [Product(**dict(row)) for row in rows]

async def get_products_by_category(category_id: int) -> List[Product]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, name, description, price, category_id FROM products WHERE category_id=$1 ORDER BY id;",
            category_id
        )
        return [Product(**dict(row)) for row in rows]

async def get_product_by_id(product_id: int) -> Optional[Product]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, name, description, price, category_id FROM products WHERE id=$1;", product_id)
        return Product(**dict(row)) if row else None

async def delete_product(product_id: int) -> bool:
    pool = await get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute("DELETE FROM products WHERE id=$1;", product_id)
        return result.startswith("DELETE")

async def update_product(product_id: int, name: str, description: Optional[str], price: float, category_id: int) -> Optional[Product]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE products
            SET name=$1, description=$2, price=$3, category_id=$4
            WHERE id=$5
            RETURNING id, name, description, price, category_id
            """, name, description, price, category_id, product_id)
        if row:
            return Product(**dict(row))
        return None
