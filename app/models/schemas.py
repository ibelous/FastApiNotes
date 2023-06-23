import datetime

from pydantic import BaseModel, Field, PositiveInt


class NoteSchema(BaseModel):
    text: str = Field(..., min_length=4)


class NoteUpdateSchema(BaseModel):
    text: str = Field(..., min_length=4)
    board: int = PositiveInt()


class NoteResponseSchema(BaseModel):
    id: int = PositiveInt()
    created_at: datetime.datetime = Field(
        ...,
    )
    modified_at: datetime.datetime = Field(
        ...,
    )
    text: str = Field(..., min_length=4)
    views_count: int = PositiveInt()


class BoardSchema(BaseModel):
    title: str = Field(..., min_length=4, max_length=128)
