from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

# PostgreSQL database URL in the format:
# postgresql://<username>:<password>@<host>:<port>/<database_name>
DATABASE_URL = "postgresql://postgres:1234567@127.0.0.1:5432/bookdb"

try:
    print("[info] Connecting to database...")  
    engine = create_engine(DATABASE_URL)
    
    # Create a session factory bound to the engine
    SessionLocal = sessionmaker(bind=engine, autoflush=False)
    
    print("✅ Database connection successful.") 
except OperationalError as e:
    print("[error] Failed to connect to the database:")  
    print(e) 
    raise  # Reraise 

# Base class for all ORM models
Base = declarative_base()

# rovide a DB session per request
def get_db():
    try:
        db = SessionLocal()  # Create DB session
        yield db  # Yield it to the request handler
    except Exception as e:
        print("[error] during DB session:", e) 
        raise  # re raise 
    finally:
        db.close()  
        print("[info] DB session closed.")  
