# 📚 Book Review API

A complete Book Review service using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Pydantic v2**, **Alembic**, and **Pytest**. This app supports adding books and reviews, calculates average ratings, and demonstrates caching using a mock in-memory dictionary.

---

## Tech Stack

* **FastAPI** – Web framework
* **PostgreSQL** – Relational database
* **SQLAlchemy** – ORM
* **Pydantic v2** – Data validation
* **Alembic** – Database migrations
* **Pytest** – Unit and integration testing
* **Mock Cache** – In-memory `dict` (for testing)

---

##  Features

*  Add and list books
*  Add and fetch reviews for a book
*  Auto-calculate average rating
*  Mock caching for performance simulation
*  Error handling and graceful fallbacks
*  Swagger-based API documentation

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd BookReview
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv

# For Unix/macOS
source venv/bin/activate

# For Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Make sure PostgreSQL is running. Create the database:

```sql
CREATE DATABASE bookdb;
```

Update your connection string in `database.py`:

```python
DATABASE_URL = "postgresql://postgres:1234567@127.0.0.1:5432/bookdb"
```

---

## ⚙️ Alembic for Migrations

### Initialize Alembic

```bash
alembic init alembic
```

### Update `alembic.ini`

In the `[alembic]` section, update the `sqlalchemy.url`:

```ini
sqlalchemy.url = postgresql://postgres:1234567@127.0.0.1:5432/bookdb
```

### Update `env.py`

Inside `alembic/env.py`, locate the line:

```python
from myapp import mymodel
```

Replace or update the `target_metadata` line to point to your actual model metadata:

```python
from app.models import base  # adjust if needed

target_metadata = base.Base.metadata
```

### Generate Migration Script

```bash
alembic revision --autogenerate -m "Initial tables and index"
```

### Apply Migration

```bash
alembic upgrade head
```

This creates all required tables and indexes for the Book and Review models.

---

## 🚀 Run the Application

```bash
uvicorn server:app --reload
```

* API Root: [http://localhost:8000](http://localhost:8000)
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Run Tests

Tests are written using **Pytest**.

```bash
pytest
```

Make sure your test files:

* Are placed inside a `/tests` directory

---

## 📖 API Documentation

Interactive API documentation is available at:

* Swagger UI: `/docs`

These are auto-generated using FastAPI’s OpenAPI integration.

---

## Mock Caching

This project uses a simple in-memory dictionary as a mock cache for books. It simulates performance boosts by avoiding repeated DB queries in tests.

```python
mock_cache = {}

def get_books_cache():
    return mock_cache.get("books")

def set_books_cache(data):
    mock_cache["books"] = data

def clear_books_cache():
    mock_cache.pop("books", None)
```

---

## 📂 Project Structure

```
BookReview/
├── alembic/
├── app/
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── database.py
│   ├── cache.py
├── tests/
├── server.py
├── requirements.txt
└── README.md
```

---

## Contributions

Feel free to open issues or submit pull requests for improvements or feature additions!

