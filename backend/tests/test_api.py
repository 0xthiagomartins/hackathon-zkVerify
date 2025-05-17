from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_list_gyms():
    response = client.get("/gyms")
    assert response.status_code == 200
    gyms = response.json()
    assert len(gyms) > 0
    assert gyms[0]["id"] == 1


def test_get_gym():
    response = client.get("/gym/1")
    assert response.status_code == 200
    gym = response.json()
    assert gym["id"] == 1
    assert gym["name"] == "Academia Central"


def test_generate_proof():
    response = client.post(
        "/generate-proof",
        json={"user_lat": 37423640, "user_long": -122084050, "gym_id": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "proof" in data
    assert "public_inputs" in data
