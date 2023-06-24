import pytest as pytest

from tests.factories.boards import BoardFactory
from tests.factories.notes import NoteFactory


@pytest.mark.asyncio()
async def test_create_note(async_client):
    board = await BoardFactory().save()
    payload = {
        "text": "example text",
        "board": board.id,
    }
    response = await async_client.post(f"/api/boards/{board.id}/notes/", json=payload)
    assert response.status_code == 201


@pytest.mark.asyncio()
async def test_get_note(async_client):
    board = await BoardFactory().save()
    note = await NoteFactory(board=board).save()
    response = await async_client.get(f"/api/boards/{board.id}/notes/{note.id}/")
    assert response.status_code == 200
    assert response.json()["text"] == note.text


@pytest.mark.asyncio()
async def test_get_notes_list(async_client):
    board = BoardFactory()
    await board.save()
    notes = NoteFactory.create_batch(5, board=board)
    for note in notes:
        await note.save()
    response = await async_client.get(f"/api/boards/{board.id}/notes/")
    assert response.status_code == 200
    assert len(response.json()) == 5


@pytest.mark.asyncio()
async def test_update_board(async_client):
    board = BoardFactory()
    await board.save()
    note = NoteFactory(board=board)
    await note.save()
    new_text = note.text + "_updated"
    payload = {
        "text": new_text,
    }
    response = await async_client.put(f"/api/boards/{board.id}/notes/{note.id}/", json=payload)
    assert response.status_code == 200
    assert response.json()["text"] == new_text
