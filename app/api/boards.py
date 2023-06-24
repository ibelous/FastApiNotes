from fastapi import APIRouter
from fastapi.responses import Response

from app.api import notes
from app.config import Board, Note
from app.models.schemas import BoardSchema

router = APIRouter()
router.include_router(notes.router, prefix="/{board_id}/notes", tags=["notes"])


@router.post("/", status_code=201)
async def create_board(board: BoardSchema):
    return await Board(**board.dict()).save()


@router.get("/", status_code=200)
async def list_boards():
    return await Board.objects.prefetch_related("notes").all()


@router.get("/{id}/", status_code=200)
async def get_board(id: int):
    if board := await Board.objects.prefetch_related("notes").get_or_none(id=id):
        return board
    return Response("Not found.", status_code=404)


@router.put("/{id}/")
async def update_board(id: int, board: BoardSchema):
    if board_db := await Board.objects.get_or_none(id=id):
        return await board_db.update(**dict(board))
    return Response("Not found.", status_code=404)


@router.delete("/{id}/")
async def delete_note(id: int):
    if note := await Note.objects.get_or_none(id=id):
        await note.delete()
        return Response(status_code=200)
    return Response("Not found.", status_code=404)
