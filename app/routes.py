from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Book, Review
from app.schemas import BookCreate, BookResponse, ReviewCreate, ReviewResponse
from app.database import get_db
from app.cache import get_books_cache, set_books_cache, clear_books_cache

book_router = APIRouter()

@book_router.get("/books", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    try:
        print("[info] Trying to fetch books from cache")
        cached = get_books_cache()
        if cached:
            print("[cache] Books found in cache. Returning cached data.")
            return cached

        print("[info] Books not in cache. Querying database...")
        books = db.query(Book).all()
        result = [BookResponse.model_validate(book) for book in books]

        if not result:
            print("[warn] No books found in database.Please Add books using POST /books.")

        print("[info] Setting fetched books to cache...")
        set_books_cache(result)

        return result

    except Exception as e:
        print("[error] Failed to fetch books:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error while fetching books.")



@book_router.post("/books")
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    try:
        if book.isbn:
            print(f"[info] Checking if book with ISBN: {book.isbn} already exists")
            existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
            if existing_book:
                print("[warn] Book already exists with this ISBN")
                raise HTTPException(status_code=400, detail="Book with this ISBN already exists")

        print("[info] Adding new book to database")
        new_book = Book(**book.model_dump())
        db.add(new_book)
        db.commit()

        print("[cache] Clearing books cache after addition")
        clear_books_cache()

        return {"message": "Book added"}

    except HTTPException as he:
        raise he  # re-raise HTTP errors
    except Exception as e:
        print("[error] Failed to add book:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error while adding book.")


@book_router.get("/books/{id}/reviews", response_model=list[ReviewResponse])
def get_reviews(id: int, db: Session = Depends(get_db)):
    try:
        print(f"[info] Fetching reviews for book ID: {id}")
        
        # Check if book exists
        book = db.query(Book).filter(Book.id == id).first()
        if not book:
            print("[warn] Book not found")
            raise HTTPException(status_code=404, detail="Book not found")

        # Fetch reviews
        reviews = db.query(Review).filter_by(book_id=id).all()

        if not reviews:
            print("[info] No reviews found for this book")
            print('[info] Please add reviews using POST /books/{id}/reviews')

        return [ReviewResponse.model_validate(r) for r in reviews]

    except HTTPException as he:
        raise he  # re raise
    except Exception as e:
        print("[error] Failed to fetch reviews:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error while fetching reviews.")


@book_router.post("/books/{id}/reviews")
def add_review(id: int, review: ReviewCreate, db: Session = Depends(get_db)):
    try:
        print(f"[info] Attempting to add review for book ID: {id}")

        # Check if book exists
        book = db.query(Book).filter(Book.id == id).first()
        if not book:
            print("[warn] Book not found")
            raise HTTPException(status_code=404, detail="Book not found")

        # Add review
        db_review = Review(content=review.content, rating=review.rating, book_id=id)
        db.add(db_review)

        # Recalculate average rating
        all_ratings = [r.rating for r in book.reviews] + [review.rating]
        book.average_rating = round(sum(all_ratings) / len(all_ratings), 2)

        db.commit()
        print("[success] Review added and average rating updated")

        clear_books_cache()
        print("[cache] Cleared book cache after adding review")

        return {"message": "Review added"}

    except HTTPException as he:
        raise he
    except Exception as e:
        print("[error] Failed to add review:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error while adding review.")

