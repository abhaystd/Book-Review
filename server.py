from fastapi import FastAPI
from app.database import Base, engine
from app.routes import book_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Include book routes
app.include_router(book_router)

# Run with: python server.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
