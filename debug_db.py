from app.core.database import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful!")
        print(f"Result: {result.fetchone()}")
except Exception as e:
    print(f"Database connection failed: {e}")
    print(f"Error type: {type(e)}")