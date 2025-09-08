from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Book(BaseModel):
    name: str
    author: str
    price: float
    rating: float
    #published: Optional[float]

books_list = [{"name": "abc", "author":"xyz", "price": 12, "rating": 3, "id": 1}, {"name": "xyz", "author":"abc", "price": 10, "rating": 2.5, "id": 2}]


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/books")
def get_books():
    return {"books": books_list}

@app.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(response: Book):
    books_list.append(response)
    return {"books": books_list}

@app.get("/books/{id}")
def get_book(id: int):
    for b in books_list:
        if b["id"] == id:
            return {"book": b}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id {id} not found")

@app.put("/books/{id}")
def update_book(id:int, response: Book):
    for i, b in enumerate(books_list):
        if b["id"] == id:
            books_list[i] = response.model_dump()
            return {"message": books_list}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no book entry for id {id}")