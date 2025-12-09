"""
Файл для создания простого API приложения для управления книгами

Автор: [Владислав Мещеряк]
Версия: 1.0
"""

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db, Book, Base, engine

Base.metadata.create_all(engine)

class BookCreate(BaseModel):
    title: str
    author: str
    year: Optional[int] = None

class BookResponse(BookCreate):
    id: int

    class Config:
        from_attributes = True

# Инициализация приложения
app = FastAPI(title="Book API", version = "1.0.0")

# Корень программы
@app.get("/")
def root():
    return {"message": "Book API is running"}

# Получение всех книг
@app.get("/books/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

# Поиск книги
@app.get("/books/search/", response_model=List[BookResponse])
def search_books(
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None,
        db: Session = Depends(get_db)):

    query = db.query(Book)

    if title: # Поиск по названию
        query = query.filter(Book.title.ilike(f"%{title}%"))

    if author: # Поиск по автору
        query = query.filter(Book.author.ilike(f"%{author}%"))

    if year: # Поиск по году выпуска
        query = query.filter(Book.year == year)

    books = query.all()
    return books

# Добавление книги
@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Обновление книги по ID
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if db_book is None:     #Если не найдено, выдать ошибку
        raise HTTPException(status_code=404, detail="Book not found")

    updated_data = book_update.dict(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(db_book, field, value)


    db.commit()
    db.refresh(db_book)

    return db_book

# Удаление книги по ID
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book is not found")

    db.delete(book)
    db.commit()

    return {"message": f"Book {book_id} deleted"}