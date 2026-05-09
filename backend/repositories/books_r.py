# Added 'delete' to the imports
from sqlmodel import Session, select, delete
from models.books import Book, BookCreate

class BookRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(self):
        statement = select(Book)
        return self.session.exec(statement).all()
    
    def get_one(self, item_id: int):
        statement = select(Book).where(Book.id == item_id)
        return self.session.exec(statement).first()

    def insert(self, payload: BookCreate):
        item = Book.model_validate(payload)
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

    # --- NEW FUNCTION ---
    def delete_all(self):
        statement = delete(Book)
        self.session.exec(statement)
        self.session.commit()
        return {"message": "All books have been deleted"}