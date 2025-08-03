# Solution Steps

1. Create a PostgreSQL schema with two tables: categories and products. The categories table has id (PK) and unique name. The products table has id (PK), name, description, price, and category_id (FK to categories). Enforce unique and required constraints as appropriate.

2. Implement database.py to provide asyncpg pool connection setup and an init_db coroutine that creates the above tables if they do not exist.

3. Create dal.py as the Data Access Layer. Implement async functions for all CRUD operations for products and categories, including create, read, update, and delete. These functions use the asyncpg connection pool from database.py.

4. Define internal lightweight Product and Category model classes in dal.py for easy data exchange.

5. Implement the FastAPI main.py application. Create and use appropriate Pydantic models for request and response validation.

6. In main.py, implement API endpoints to add and list categories, get a category by id, add and list products, get a product by id, and list products by category. Use functions from the DAL.

7. Ensure that at startup, your application initializes the database schema using the startup event in FastAPI, calling init_db() from database.py.

8. All interactions with the database are performed via async/await and the asyncpg pool, providing end-to-end non-blocking support.

9. Test the API by issuing requests to add categories, add products (with valid category_id), retrieve all products, and retrieve products by a specific category, confirming that data is persisted and the schema is enforced in the database.

