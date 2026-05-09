from typing import Optional
from sqlmodel import Field, SQLModel

# We add year_of_production here
class BookBase(SQLModel):
    title: str
    genre: str
    year_of_production: int
    author_id: int = Field(foreign_key="authors.id") 

class Book(BookBase, table=True):
    __tablename__ = "books"
    id: Optional[int] = Field(default=None, primary_key=True)

class BookCreate(BookBase):
    pass