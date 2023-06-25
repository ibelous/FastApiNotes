from fastapi import APIRouter
from fastapi.responses import Response

from app.config import Board, Note
from app.models.schemas import NoteResponseSchema, NoteSchema, NoteUpdateSchema

router = APIRouter()


@router.post("/", status_code=201, response_model=Note)
async def create_note(board_id: int, note: NoteSchema):
    if not await Board.objects.filter(id=board_id).exists():
        return Response("Not found.", status_code=404)
    note_dict = note.dict()
    note_dict.update({"board": board_id})
    return await Note(**note_dict).save()


@router.get("/", status_code=200, response_model=list[NoteResponseSchema])
async def list_notes(board_id: int):
    if not await Board.objects.filter(id=board_id).exists():
        return Response("Not found.", status_code=404)
    return await Note.objects.filter(board__id=board_id).all()


@router.get("/{id}/", status_code=200, response_model=NoteResponseSchema)
async def get_note(board_id: int, id: int):
    if note := await Note.objects.get_or_none(board__id=board_id, id=id):
        return await note.update(views_count=note.views_count + 1)
    return Response("Not found.", status_code=404)


@router.put("/{id}/")
async def update_note(board_id: int, id: int, note: NoteUpdateSchema):
    if note_db := await Note.objects.get_or_none(board__id=board_id, id=id):
        return await note_db.update(**dict(note))
    return Response("Not found.", status_code=404)


@router.delete("/{id}/")
async def delete_note(id: int):
    if note := await Note.objects.get_or_none(id=id):
        await note.delete()
        return Response(status_code=200)
    return Response("Not found.", status_code=404)
