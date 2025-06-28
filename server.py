from fastapi import FastAPI
from app.database import Base, engine
from app.routes import book_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Include book routes
app.include_router(book_router)

@app.get("/")
def testserver():
    return {"status" :200,"details":"server is running"}

# # In root directory 

# if you migrating, this will run the initial migration
# You can run the following command to create the initial migration:
# alembic revision --autogenerate -m "Initial tables and index"
# and then apply it with:
# alembic upgrade head

# To run the server, you can use the command below.
# uvicorn server:app --reload or python server.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
