from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from database_model import Product as ProductModel, Base
# use Pydantic schema for request/response validation
from models import Product as ProductSchema
from sqlalchemy.orm import Session

app = FastAPI()

# 🔹 FRONTEND CONNECTION: CORS middleware setup to allow React frontend (port 3000) to access this API
# Without this, browser would block requests due to same-origin policy
origins = [
    "http://localhost:3000",  # React development server
    # add other origins if you deploy the frontend elsewhere
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Allow these frontend URLs to access API
    allow_credentials=True,     # Allow cookies/auth headers
    allow_methods=["*"],        # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],        # Allow all headers in requests
)

# 🔹 DATABASE CONNECTION: Create database tables if they don't exist
# This connects to database using engine from database.py
Base.metadata.create_all(bind=engine)

# List of data
products = [
    {"id": 1, "name": "laptop", "description": "High performance laptop", "price": 60000, "quantity": 50},
    {"id": 2, "name": "gaming laptop", "description": "Powerful laptop for gaming", "price": 120000, "quantity": 30},
    {"id": 3, "name": "macbook", "description": "Best laptop for programming", "price": 150000, "quantity": 20},
    {"id": 4, "name": "business laptop", "description": "Lightweight office laptop", "price": 90000, "quantity": 10},
    {"id": 5, "name": "ultrabook", "description": "Slim and portable laptop", "price": 80000, "quantity": 15}
]

# 🔹 DATABASE CONNECTION: Dependency function that creates new database session for each request
# Each request gets its own database connection which is closed after request completes
def get_db():
    db = SessionLocal()  # Create new database session
    try:
        yield db  # Provide session to the endpoint
    finally:
        db.close()  # Always close session even if error occurs

# 🔹 DATABASE CONNECTION: Initialize database with sample data
# This function connects to DB and inserts initial products if they don't exist
def init_db():
    db = SessionLocal()  # Create database connection
    for item in products:
        # Check if product already exists in database
        existing = db.query(ProductModel).filter(ProductModel.id == item["id"]).first()
        if not existing:
            db.add(ProductModel(**item))  # Insert new product
    db.commit()  # Save all changes to database
    db.close()  # Close database connection

# Insert data as soon as the server starts
init_db()


@app.get("/")
def home():
    return {"message": "Welcome to Laptop Product API"}


# 🔹 FRONTEND CONNECTION: GET endpoint that frontend calls to fetch all products
# Returns list of products that React will display
@app.get("/products", response_model=list[ProductSchema])
def get_products(db: Session = Depends(get_db)):  # Database session injected here
    db_products = db.query(ProductModel).all()  # Query database for all products
    return db_products  # Send data back to frontend

# alias for GET /products/{id} to match frontend expectations
@app.get("/products/{id}", response_model=ProductSchema)
def get_product_by_id_alias(id: int, db: Session = Depends(get_db)):
    return get_product_by_id(id, db)

# 🔹 FRONTEND CONNECTION: GET single product by ID
# Frontend calls this when viewing product details
@app.get("/product/{id}", response_model=ProductSchema)
def get_product_by_id(id: int, db: Session = Depends(get_db)):  # Database session injected
    db_product = db.query(ProductModel).filter(ProductModel.id == id).first()  # Query DB for specific product
    if db_product:
        return db_product  # Send product data to frontend
    raise HTTPException(status_code=404, detail="Product not found")  # Error if product doesn't exist

# 🔹 FRONTEND CONNECTION: POST endpoint for adding new products
# Frontend sends product data here when user adds a product
@app.post("/product", response_model=ProductSchema)
def add_product(product: ProductSchema, db: Session = Depends(get_db)):  # Get data from frontend & DB connection
    # check for duplicates
    existing = db.query(ProductModel).filter(ProductModel.id == product.id).first()  # Check if ID already exists
    if existing:
        raise HTTPException(status_code=400, detail="Product with this ID already exists")  # Error if duplicate

    db_product = ProductModel(**product.dict())  # Convert frontend data to database model
    db.add(db_product)  # Add to database session
    db.commit()  # Save to database
    db.refresh(db_product)  # Get updated data from database
    # return the newly created object; FastAPI will convert it using response_model
    return db_product  # Send created product back to frontend

# alias to satisfy frontend that posts to /products
@app.post("/products", response_model=ProductSchema)
def add_product_alias(product: ProductSchema, db: Session = Depends(get_db)):
    return add_product(product, db)


# 🔹 FRONTEND CONNECTION: PUT endpoint for updating existing products
# Frontend sends updated data here when user edits a product
@app.put("/product/{id}", response_model=ProductSchema)
def update_product(id: int, updated_product: ProductSchema, db: Session = Depends(get_db)):  # Get ID, frontend data, DB connection
    product = db.query(ProductModel).filter(ProductModel.id == id).first()  # Find product in database
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")  # Error if product doesn't exist

    # Update product fields with data from frontend
    product.name = updated_product.name
    product.description = updated_product.description
    product.price = updated_product.price
    product.quantity = updated_product.quantity

    db.commit()  # Save changes to database
    db.refresh(product)  # Get updated data
    return product  # Send updated product back to frontend

# alias so frontend requests using /products/{id} also work for update
@app.put("/products/{id}", response_model=ProductSchema)
def update_product_alias(id: int, updated_product: ProductSchema, db: Session = Depends(get_db)):
    return update_product(id, updated_product, db)


# 🔹 FRONTEND CONNECTION: DELETE endpoint for removing products
# Frontend calls this when user deletes a product
@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):  # Get product ID from URL and DB connection
    product = db.query(ProductModel).filter(ProductModel.id == id).first()  # Find product in database
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")  # Error if product doesn't exist
    db.delete(product)  # Mark for deletion
    db.commit()  # Remove from database
    return {"message": "Product deleted successfully"}  # Send confirmation to frontend

# alias so frontend requests using /products/{id} also work for delete
@app.delete("/products/{id}")
def delete_product_alias(id: int, db: Session = Depends(get_db)):
    return delete_product(id, db)