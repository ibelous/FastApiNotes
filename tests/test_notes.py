import pytest as pytest

from app.config import Note
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
async def test_get_note_valid(async_client):
    board = await BoardFactory().save()
    note = await NoteFactory(board=board).save()
    response = await async_client.get(f"/api/boards/{board.id}/notes/{note.id}/")
    assert response.status_code == 200
    assert response.json()["text"] == note.text


@pytest.mark.asyncio()
async def test_get_note_invalid_board_id(async_client):
    board = await BoardFactory().save()
    note = await NoteFactory(board=board).save()
    response = await async_client.get(f"/api/boards/{board.id+123}/notes/{note.id}/")
    assert response.status_code == 404


@pytest.mark.asyncio()
async def test_get_note_invalid_note_id(async_client):
    board = await BoardFactory().save()
    note = await NoteFactory(board=board).save()
    response = await async_client.get(f"/api/boards/{board.id}/notes/{note.id+123}/")
    assert response.status_code == 404


@pytest.mark.asyncio()
async def test_get_notes_list_valid(async_client):
    board = BoardFactory()
    await board.save()
    notes = NoteFactory.create_batch(5, board=board)
    for note in notes:
        await note.save()
    response = await async_client.get(f"/api/boards/{board.id}/notes/")
    assert response.status_code == 200
    assert len(response.json()) == 5


@pytest.mark.asyncio()
async def test_get_notes_list_invalid_board_id(async_client):
    board = BoardFactory()
    await board.save()
    notes = NoteFactory.create_batch(5, board=board)
    for note in notes:
        await note.save()
    response = await async_client.get(f"/api/boards/{board.id+123}/notes/")
    assert response.status_code == 404


@pytest.mark.asyncio()
async def test_update_note_valid(async_client):
    board = BoardFactory()
    await board.save()
    note = NoteFactory(board=board)
    await note.save()
    old_modified_at = note.modified_at
    old_created_at = note.created_at
    new_text = note.text + "_updated"
    payload = {
        "text": new_text,
    }
    response = await async_client.put(f"/api/boards/{board.id}/notes/{note.id}/", json=payload)
    assert response.status_code == 200
    assert response.json()["text"] == new_text
    note = await Note.objects.get(id=note.id)
    assert old_created_at == note.created_at
    assert old_modified_at != note.modified_at


@pytest.mark.asyncio()
async def test_update_note_invalid_board_id(async_client):
    board = BoardFactory()
    await board.save()
    note = NoteFactory(board=board)
    await note.save()
    old_text = note.text
    new_text = note.text + "_updated"
    payload = {
        "text": new_text,
    }
    response = await async_client.put(f"/api/boards/{board.id+123}/notes/{note.id}/", json=payload)
    assert response.status_code == 404
    note = await Note.objects.get(id=note.id)
    assert note.text == old_text


@pytest.mark.asyncio()
async def test_update_note_invalid_note_id(async_client):
    board = BoardFactory()
    await board.save()
    note = NoteFactory(board=board)
    await note.save()
    old_text = note.text
    new_text = note.text + "_updated"
    payload = {
        "text": new_text,
    }
    response = await async_client.put(f"/api/boards/{board.id}/notes/{note.id+123}/", json=payload)
    assert response.status_code == 404
    note = await Note.objects.get(id=note.id)
    assert note.text == old_text


@pytest.mark.asyncio()
async def test_get_note_views_count(async_client):
    board = await BoardFactory().save()
    note = await NoteFactory(board=board).save()
    assert note.views_count == 0
    views = 5
    for i in range(views):
        response = await async_client.get(f"/api/boards/{board.id}/notes/{note.id}/")
        assert response.status_code == 200
        note = await Note.objects.get(id=note.id)
        assert note.views_count == i + 1
