import pytest as pytest

from app.config import Board
from tests.factories.boards import BoardFactory


@pytest.mark.asyncio()
async def test_create_board(async_client):
    payload = {
        "title": "example"
    }
    response = await async_client.post("api/boards/", json=payload)
    assert response.status_code == 201
    assert await Board.objects.count() == 1


@pytest.mark.asyncio()
async def test_get_board(async_client):
    board = BoardFactory()
    await board.save()
    response = await async_client.get(f"/api/boards/{board.id}/")
    assert response.status_code == 200

@pytest.mark.asyncio()
async def test_get_boards_list(async_client):
    boards = BoardFactory.create_batch(5)
    for b in boards:
        await b.save()
    response = await async_client.get("/api/boards/")
    assert response.status_code == 200
    assert len(response.json()) == 5

@pytest.mark.asyncio()
async def test_update_board(async_client):
    board = BoardFactory()
    await board.save()
    new_title = board.title + "_updated"
    payload = {
        "title": new_title,
    }
    response = await async_client.put("/api/boards/1/", json=payload)
    assert response.status_code == 200
    assert new_title == response.json()["title"]