from fastapi import FastAPI
from routers.authors_ro import router as authors_router
from routers.books_ro import router as books_router
from database import start_db

# Create the database tables when the app launches
start_db()

# Initialize the FastAPI app
app = FastAPI(title="Library API")

# Plug in the routers
app.include_router(authors_router)
app.include_router(books_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Library API!"}