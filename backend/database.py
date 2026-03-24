from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import time, os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://velai:velai@localhost:5432/velai")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_db():
    # Wait for the DB to be ready
    retries = 5
    while retries > 0:
        try:
            with engine.connect() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                conn.commit()
            break
        except Exception as e:
            print(f"Database connection failed. Retrying... ({retries})")
            retries -= 1
            time.sleep(2)
            if retries == 0:
                print("Could not connect to the database after multiple attempts.")
                raise e

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()