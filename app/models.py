from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    published_year= Column(Integer, nullable=True)
    genres = Column(String, nullable=False)
    recommend = Column(Boolean, server_default='False', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
