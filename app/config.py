import datetime
import os

import ormar
from databases import Database
from dotenv import load_dotenv
from pydantic import BaseSettings, Field
from sqlalchemy import MetaData, func


class Settings(BaseSettings):
    db_url: str = Field(..., env="DATABASE_URL")


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://backend:backend@db:5432/backend")
DATABASE_PATH = DATABASE_URL.replace("postgresql://", "")

metadata = MetaData()


database = Database(DATABASE_URL)
settings = Settings()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Board(ormar.Model):
    class Meta(BaseMeta):
        tablename = "boards"

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=128)
    created_at: datetime.datetime = ormar.DateTime(server_default=func.now())
    modified_at: datetime.datetime = ormar.DateTime(server_default=func.now())


class Note(ormar.Model):
    class Meta(BaseMeta):
        tablename = "notes"

    id: int = ormar.Integer(primary_key=True)
    text: str = ormar.Text()
    created_at: datetime.datetime = ormar.DateTime(server_default=func.now())
    modified_at: datetime.datetime = ormar.DateTime(server_default=func.now())
    views_count: int = ormar.Integer(minimum=0, default=0)
    board = ormar.ForeignKey(Board, related_name="notes")


@ormar.pre_update([Note, Board])
async def before_update(sender, instance, **kwargs):
    if sender == Note and "passed_args" in kwargs and "views_count" in kwargs["passed_args"]:
        return
    instance.modified_at = datetime.datetime.now()


@ormar.pre_save([Note, Board])
async def before_save(sender, instance, **kwargs):
    now = datetime.datetime.now()
    instance.created_at = now
    instance.modified_at = now
