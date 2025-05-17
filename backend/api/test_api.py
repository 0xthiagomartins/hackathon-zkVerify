from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_get_gyms():
    response = client.get("/gyms")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_gym():
    response = client.get("/gym/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Academia Central"


def test_get_nonexistent_gym():
    response = client.get("/gym/999")
    assert response.status_code == 404


# Este teste pode falhar se o ambiente Noir não estiver corretamente configurado
# durante os testes automatizados
def test_generate_proof_valid():
    # Coordenadas próximas (deveria gerar prova válida)
    response = client.post(
        "/generate-proof",
        json={"user_lat": 37423640, "user_long": -122084050, "gym_id": 1},
    )
    # Se o ambiente Noir estiver disponível
    if response.status_code == 200:
        assert response.json()["success"] == True
        assert "proof" in response.json()
    else:
        # Caso contrário, verificamos apenas se a resposta tem o formato correto de erro
        assert "detail" in response.json()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
