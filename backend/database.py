import os
from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

# Load the variables from the .env file
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")

# Build the connection URL
DATABASE_URL = (
    f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Create the engine (the core connection point)
engine = create_engine(DATABASE_URL)

# This function provides a database session for our API routes
def get_session():
    with Session(engine) as session:
        yield session

# This function creates the tables when the app starts
def start_db():
    SQLModel.metadata.create_all(engine)