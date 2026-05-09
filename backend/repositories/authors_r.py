# Notice we added 'delete' to the imports here
from sqlmodel import Session, select, delete
from models.authors import Author, AuthorCreate

class AuthorRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(self):
        statement = select(Author)
        return self.session.exec(statement).all()
    
    def get_one(self, item_id: int):
        statement = select(Author).where(Author.id == item_id)
        return self.session.exec(statement).first()

    def insert(self, payload: AuthorCreate):
        item = Author.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, item_id: int):
        item = self.get_one(item_id)
        if item:
            self.session.delete(item)
            self.session.commit()
        return item

  
    def delete_all(self):
        statement = delete(Author)
        self.session.exec(statement)
        self.session.commit()
        return {"message": "All authors have been deleted"}