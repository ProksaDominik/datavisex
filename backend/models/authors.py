from typing import Optional
from sqlmodel import Field, SQLModel

# We add age and country here
class AuthorBase(SQLModel):
    name: str
    bio: str
    age: int
    country: str

class Author(AuthorBase, table=True):
    __tablename__ = "authors"
    id: Optional[int] = Field(default=None, primary_key=True)

class AuthorCreate(AuthorBase):
    pass