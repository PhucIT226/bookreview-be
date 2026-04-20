from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="dist", html=True), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


@app.post("/books")
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get("/books/{id}")
def get_book(id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == id).first()


@app.post("/reviews")
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    new_review = models.Review(**review.dict())
    db.add(new_review)
    db.commit()
    return new_review


@app.get("/books/{id}/reviews")
def get_reviews(id: int, db: Session = Depends(get_db)):
    return db.query(models.Review).filter(models.Review.book_id == id).all()
