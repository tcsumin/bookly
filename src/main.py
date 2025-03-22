from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router

version = "v1"

description = """
REST API for book reviews.
"""

version_prefix = f"/api/{version}"

app = FastAPI(
    title="Bookly",
    description=description,
    version=version
)

@app.get('/')
def hello():
    return {"message": "Hello!!"}

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

app.include_router(book_router, prefix=f"{version_prefix}/books", tags=["books"])
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])