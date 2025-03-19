from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Book

app = FastAPI()

# Tables
Base.metadata.create_all(bind=engine)

# Connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def home():
    return {"message": "Hello"}

@app.get("/books")
def get_books(
    db: Session = Depends(get_db),
    category: str = Query(None, description="Filter by category"),
    min_stars: int = Query(None, description="Minimum stars"),
    max_price: float = Query(None, description="Maximum price"),
    availability: str = Query(None, description="Filter by availability")
):
    query = db.query(Book)

    # Apply filters
    if category:
        query = query.filter(Book.category.ilike(f"%{category}%"))
    
    if min_stars is not None:
        query = query.filter(Book.stars >= min_stars)

    if max_price is not None:
        query = query.filter(Book.price <= max_price)

    if availability:
        query = query.filter(Book.availability.ilike(f"%{availability}%"))

    books = query.all()
    return books

