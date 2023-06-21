"""Main application and routing logic for CacheChat API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .internal import admin
from .routers import items, users

app = FastAPI()
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Paths
@app.get("/")
async def read_root() -> dict[str, str]:
    """Read root.

    Returns
    -------
    dict[str, str]
        Message
    """
    return {"message": "CacheChat API"}
