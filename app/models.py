from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Date, Index
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published_date = Column(Date, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    genre = Column(String)
    price = Column(Float)
    average_rating = Column(Float, default=0.0)

    reviews = relationship("Review", back_populates="book", cascade="all, delete")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    book = relationship("Book", back_populates="reviews")

Index("ix_reviews_book_id", Review.book_id)

