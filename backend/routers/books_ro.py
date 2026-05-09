from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models.books import Book, BookCreate
from repositories.books_r import BookRepository

router = APIRouter(prefix="/books", tags=["Books"])

def get_book_repository(session: Annotated[Session, Depends(get_session)]) -> BookRepository:
    return BookRepository(session)

@router.get("/", response_model=List[Book])
async def get_books(repo: Annotated[BookRepository, Depends(get_book_repository)]):
    return repo.get_all()

@router.get("/{id}", response_model=Book)
async def get_book(id: int, repo: Annotated[BookRepository, Depends(get_book_repository)]):
    item = repo.get_one(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return item

@router.post("/", response_model=Book)
async def add_book(book: BookCreate, repo: Annotated[BookRepository, Depends(get_book_repository)]):
    return repo.insert(book)

@router.delete("/{id}", response_model=Book)
async def delete_book(id: int, repo: Annotated[BookRepository, Depends(get_book_repository)]):
    item = repo.delete(id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Book with id {id} does not exist")
    return item

@router.delete("/")
async def delete_all_books(repo: Annotated[BookRepository, Depends(get_book_repository)]):
    return repo.delete_all()