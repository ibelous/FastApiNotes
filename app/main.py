from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import boards
from app.config import BaseMeta, database
from app.migrations import apply_migrations

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    apply_migrations(str(BaseMeta.database.url))
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.get("/api/healthchecker")
def root():
    return {"message": "The API is LIVE!!"}


app.include_router(boards.router, prefix="/api/boards", tags=["boards"])
