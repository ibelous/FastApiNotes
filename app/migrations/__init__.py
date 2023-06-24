from functools import wraps
from pathlib import Path

import sqlalchemy
from alembic import command as alembic
from alembic.config import Config
from loguru import logger

from app.config import DATABASE_URL, DATABASE_PATH, BaseMeta


def get_alembic_config(db_url: str = DATABASE_PATH) -> Config:
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "app:migrations")
    alembic_cfg.set_main_option("sqlalchemy.url", str(db_url))
    return alembic_cfg


def upgrade_database(revision: str = "head", db_url: str = DATABASE_PATH) -> None:
    alembic_cfg = get_alembic_config(db_url)
    alembic.upgrade(alembic_cfg, revision)


def stamp_database(revision: str = "head", db_url: str = DATABASE_PATH) -> None:
    alembic_cfg = get_alembic_config(db_url)
    alembic.stamp(alembic_cfg, revision)


def create_database(db_url: str = DATABASE_PATH) -> None:
    engine = sqlalchemy.create_engine(db_url)
    BaseMeta.metadata.create_all(engine)


def db_lock(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        lock = Path(DATABASE_URL).parent / ".dblock"
        try:
            lock.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            logger.debug("Migrations are already being applied")
            return
        logger.debug("Applying migrations")
        try:
            func(*args, **kwargs)
        finally:
            lock.rmdir()

    return wrapper


@db_lock
def apply_migrations(db_url: str = DATABASE_PATH) -> None:
    if Path(DATABASE_URL).exists():
        upgrade_database(db_url=db_url)
    else:
        create_database(db_url=db_url)
        stamp_database(db_url=db_url)