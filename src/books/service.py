from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from datetime import datetime

from src.db.models import Book
from src.books.schemas import BookCreateModel, BookUpdateModel

class BookService:
    async def get_all_books(self, session:AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uid:str, session:AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
    
        return book if book is not None else None
    
    async def create_book(
            self, 
            book_data:BookCreateModel, 
            session:AsyncSession
            ):
        book_data_dict = book_data.model_dump()   # get data in form of dictionary

        new_book = Book(**book_data_dict)
        
        new_book.published_date = datetime.strptime(book_data_dict['published_date'], "%Y-%m-%d")
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(self, book_uid:str, update_data:BookUpdateModel, session:AsyncSession):
        book_to_update = self.get_book(book_uid, session)
        if book_to_update is not None:
            book_update_data_dict = update_data.model_dump

            for k, v in book_update_data_dict.item():
                setattr(book_to_update, k, v)

            await session.commit()
            return book_to_update
        else:
            return None
    
    async def delete_book(self, book_uid:str, session:AsyncSession):
        book_to_delete = self.get_book(book_uid, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return {}
        else:
            return None