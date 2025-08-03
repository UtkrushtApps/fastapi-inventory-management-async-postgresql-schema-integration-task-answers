
import asyncpg
from typing import Optional

DATABASE_URL = "postgresql://postgres:password@localhost:5432/inventory_db"

_pool: Optional[asyncpg.pool.Pool] = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)
    return _pool

async def init_db():
    pool = await get_pool()
    async with pool.acquire() as conn:
        # Create tables: categories, products
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL
            );
        ''')
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description VARCHAR(255),
                price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
                category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE
            );
        ''')
