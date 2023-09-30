import os

import uvicorn
from sqlmodel import SQLModel

import data.allmodels
from data.databaseservice import DatabaseService

from services.service import APIService

database_service = DatabaseService(
    f"postgresql+asyncpg://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@81.200.149.171:5432/{os.environ['POSTGRES_DB']}")
# TODO убрать на проде
database_service.reset()
api = APIService(database_service)


@api.app.on_event("startup")
async def init_db():
    async with database_service.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@api.app.get("/api/status")
async def root():
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:api.app", port=5000, reload=True, workers=1)
