import datetime
import os

import ormar
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
from databases import Database
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://backend:backend@db:5432/backend")

engine = create_engine(DATABASE_URL)
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
    created_at = ormar.DateTime(default=datetime.datetime.now())
    modified_at = ormar.DateTime(default=datetime.datetime.now())


class Note(ormar.Model):
    class Meta(BaseMeta):
        tablename = "notes"

    id: int = ormar.Integer(primary_key=True)
    text: str = ormar.Text()
    created_at = ormar.DateTime(default=datetime.datetime.now())
    modified_at = ormar.DateTime(default=datetime.datetime.now())
    views_count: int = ormar.Integer(minimum=0, default=0)
    board = ormar.ForeignKey(Board, related_name="notes")


@ormar.pre_update([Note, Board])
async def before_update(sender, instance, **kwargs):
    if sender == Note and "passed_args" in kwargs and "views_count" in kwargs["passed_args"]:
        return
    instance.modified_at = datetime.datetime.now()


metadata.create_all(engine)
