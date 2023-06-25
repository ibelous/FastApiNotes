import pytest as pytest

from app.config import Board
from tests.factories.boards import BoardFactory


@pytest.mark.asyncio()
async def test_create_board(async_client):
    payload = {"title": "example"}
    response = await async_client.post("api/boards/", json=payload)
    assert response.status_code == 201
    assert await Board.objects.count() == 1


@pytest.mark.asyncio()
async def test_get_board_valid(async_client):
    board = BoardFactory()
    await board.save()
    response = await async_client.get(f"/api/boards/{board.id}/")
    assert response.status_code == 200


@pytest.mark.asyncio()
async def test_get_board_invalid(async_client):
    response = await async_client.get("/api/boards/1234/")
    assert response.status_code == 404


@pytest.mark.asyncio()
async def test_get_boards_list(async_client):
    boards = BoardFactory.create_batch(5)
    for b in boards:
        await b.save()
    response = await async_client.get("/api/boards/")
    assert response.status_code == 200
    assert len(response.json()) == 5


@pytest.mark.asyncio()
async def test_update_board_valid(async_client):
    board = BoardFactory()
    await board.save()
    old_modified_at = board.modified_at
    old_created_at = board.created_at
    new_title = board.title + "_updated"
    payload = {
        "title": new_title,
    }
    response = await async_client.put(f"/api/boards/{board.id}/", json=payload)
    board = await Board.objects.get(id=board.id)
    assert response.status_code == 200
    assert new_title == response.json()["title"]
    assert old_created_at == board.created_at
    assert old_modified_at != board.modified_at


@pytest.mark.asyncio()
async def test_update_board_invalid(async_client):
    payload = {
        "title": "new_title",
    }
    response = await async_client.put("/api/boards/1234/", json=payload)
    assert response.status_code == 404


@pytest.mark.asyncio()
async def test_delete_board_valid(async_client):
    board = BoardFactory()
    await board.save()
    response = await async_client.delete(f"/api/boards/{board.id}/")
    assert response.status_code == 200


@pytest.mark.asyncio()
async def test_delete_board_invalid(async_client):
    response = await async_client.delete("/api/boards/1234/")
    assert response.status_code == 404
