import os


def connect_to_db():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables.")
    
    print("Connecting to database...")
    return db_url

database_url = connect_to_db() 