from fastapi.testclient import TestClient

from server import app
from app.database import SessionLocal
from app.models import Book, Review

client = TestClient(app)

def test_full_book_and_review_flow():
    test_isbn = "9999999999999"
    db = SessionLocal()
    book_id = None

    try:
        #  Step 1: Add a book
        #  tesing post route /books
        response = client.post("/books", json={   
            "title": "Integrated Test Book with the help of pytest",
            "author": "Test Author",
            "genre": "Test",
            "price": 123.45,
            "published_date": "2024-01-01",
            "isbn": test_isbn
        })
        assert response.status_code == 200

        #  Step 2: Get the book ID
        book = db.query(Book).filter(Book.isbn == test_isbn).first()
        assert book is not None
        book_id = book.id

        #  Step 3: Add a review
        #  tesing post route /books/{id}/reviews
        response = client.post(f"/books/{book_id}/reviews", json={
            "content": "Excellent integration test.",
            "rating": 4.5
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Review added"

        #  Step 4: Fetch reviews
        # tesing get route /books/{id}/reviews
        response = client.get(f"/books/{book_id}/reviews")
        assert response.status_code == 200
        reviews = response.json()
        assert isinstance(reviews, list)
        assert any(r["content"] == "Excellent integration test." and r["rating"] == 4.5 for r in reviews)

        #  Step 5: Get all books (should contain ours)
        # tesing get route /books
        response = client.get("/books")
        assert response.status_code == 200
        books = response.json()
        assert any(book["title"] == "Integrated Test Book with the help of pytest" for book in books)

    finally:
        #  Cleanup: delete review(s) and book
        # Ensure we clean up the test data
        
        if book_id:
            try:
                # First attempt to clean
                db.query(Review).filter(Review.book_id == book_id).delete()
                db.query(Book).filter(Book.id == book_id).delete()
                db.commit()
            except Exception as cleanup_error:
                print("[warn] Cleanup failed on first try:", cleanup_error)
                try:
                    # Reconnect and retry cleanup
                    db = SessionLocal()
                    db.query(Review).filter(Review.book_id == book_id).delete()
                    db.query(Book).filter(Book.id == book_id).delete()
                    db.commit()
                except Exception as retry_error:
                    print("[error] Cleanup retry failed:", retry_error)
                finally:
                    db.close()
            else:
                db.close()



