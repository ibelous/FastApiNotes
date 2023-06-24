
from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/api/healthchecker")
    assert response.status_code == 200
    assert response.json() == {"message": "The API is LIVE!!"}
