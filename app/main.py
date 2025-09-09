from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db

app = FastAPI()

#this code creates all the tables defined in models
models.Base.metadata.create_all(bind=engine)

# we refer this in the function parameter, defining as pydantic code structure
#----- Schema ------#
class Book(BaseModel):
    title: str
    author: str
    price: float
    genres: str
    published_year: int

@app.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(response: Book, db:Session = Depends(get_db)):

    # instead of typing all column names and assigning to the input value, we use pydantic code (** & model_dump) to unpack all columns passed.
    new_book = models.Book(**response.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"book": new_book}

@app.get("/books/{id}")
def get_book(id: int, db:Session = Depends(get_db)):
    # .filter() is like 'where' clause
    book_id = db.query(models.Book).filter(models.Book.id == id).first()
    if not book_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id {id} not found")
    
    return {"book": book_id}

@app.put("/books/{id}")
def update_book(id:int, response: Book, db:Session = Depends(get_db)):
    # this is just a query. unless we do .all or .first, it is not running anything or giving us row
    book_query = db.query(models.Book).filter(models.Book.id == id)
    book = book_query.first()

    if book == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no book entry for id {id}")
    
    book_query.update(response.model_dump())
    db.commit()
    return {"updated book": book_query.first()}

@app.delete("/books/{id}")
def delete(id: int, db:Session = Depends(get_db)):
    book_id = db.query(models.Book).filter(models.Book.id == id)

    if book_id.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no book entry for id {id}")
    
    book_id.delete(synchronize_session = False)
    db.commit()

@app.get('/books')
# creates a database session for this api and closes it automatically once this api is closed
def get_all_books(db:Session = Depends(get_db)):
    books = db.query(models.Book).all()
    print(books)
    return {"data": books}