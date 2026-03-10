from sqlalchemy import create_engine          # Database engine banane ke liye
from sqlalchemy.ext.declarative import declarative_base  # Base banane ke liye
from sqlalchemy.orm import sessionmaker       # Database session create karne ke liye

# PostgreSQL database URL
db_url = "postgresql://postgres:root@localhost:5432/laptop_product_db"

# Database engine banaya, ye PostgreSQL se connect karega
engine = create_engine(db_url)

# SessionLocal: ye database session banayega (data insert/update/delete ke liye)
SessionLocal = sessionmaker(
    autocommit=False,      # changes manually commit karna hoga
    autoflush=False,       # flush automatically nahi hoga
    bind=engine
)

# 👇 Ye line missing thi (IMPORTANT)
Base = declarative_base()