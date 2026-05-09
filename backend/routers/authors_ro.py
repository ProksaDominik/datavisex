from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models.authors import Author, AuthorCreate
from repositories.authors_r import AuthorRepository

# Create the router. This adds the /authors prefix to all URLs here.
router = APIRouter(prefix="/authors", tags=["Authors"])

# This helper function ensures we get a fresh database connection for each request
def get_author_repository(session: Annotated[Session, Depends(get_session)]) -> AuthorRepository:
    return AuthorRepository(session)

@router.get("/", response_model=List[Author])
async def get_authors(repo: Annotated[AuthorRepository, Depends(get_author_repository)]):
    return repo.get_all()

@router.get("/{id}", response_model=Author)
async def get_author(id: int, repo: Annotated[AuthorRepository, Depends(get_author_repository)]):
    item = repo.get_one(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return item

@router.post("/", response_model=Author)
async def add_author(author: AuthorCreate, repo: Annotated[AuthorRepository, Depends(get_author_repository)]):
    return repo.insert(author)

@router.delete("/{id}", response_model=Author)
async def delete_author(id: int, repo: Annotated[AuthorRepository, Depends(get_author_repository)]):
    item = repo.delete(id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Author with id {id} does not exist")
    return item

@router.delete("/")
async def delete_all_authors(repo: Annotated[AuthorRepository, Depends(get_author_repository)]):
    return repo.delete_all()