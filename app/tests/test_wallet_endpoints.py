import pytest
from fastapi.testclient import TestClient
from uuid import UUID

from app.main import app
from app.api.endpoints.auth import get_current_user


@pytest.fixture(autouse=True, scope="session")
def override_get_current_user():
    """Подменяем зависимость get_current_user."""
    async def fake_user():
        class User:
            id = 1
            email = "test@example.com"
        return User()
    from app.main import app
    app.dependency_overrides[get_current_user] = fake_user
    yield
    app.dependency_overrides = {}


@pytest.fixture(scope="module")
def client():
    """Тестовый клиент."""
    with TestClient(app) as ac:
        yield ac


def test_create_wallet(client):
    """Тест создания кошелька."""
    resp = client.post("/api/v1/wallets")
    assert resp.status_code == 200
    data = resp.json()
    assert "uuid" in data
    assert "balance" in data
    assert data["balance"] == "0.00"

    # Проверим, что uuid валидный
    UUID(data["uuid"])


def test_get_wallet(client):
    """Тест получения кошелька."""
    # Сначала создаём кошелек
    resp = client.post("/api/v1/wallets")
    wallet = resp.json()
    wallet_uuid = wallet["uuid"]

    # Получаем кошелек
    resp = client.get(f"/api/v1/wallets/{wallet_uuid}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["uuid"] == wallet_uuid
    assert data["balance"] == "0.00"


def test_deposit_and_withdraw(client):
    """Тест депозита и вывода."""
    # Создаём кошелек
    resp = client.post("/api/v1/wallets")
    wallet_uuid = resp.json()["uuid"]

    # Делаем депозит
    resp = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000}
    )
    assert resp.status_code == 200
    assert resp.json()["balance"] == "1000.00"

    # Делаем вывод
    resp = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": 500}
    )
    assert resp.status_code == 200
    assert resp.json()["balance"] == "500.00"


def test_withdraw_insufficient_funds(client):
    """Тест недостаточных средств."""
    # Создаём кошелек
    resp = client.post("/api/v1/wallets")
    wallet_uuid = resp.json()["uuid"]

    # Пытаемся вывести больше, чем есть
    resp = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": 100}
    )
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Insufficient funds"


def test_invalid_operation_type(client):
    """Тест недопустимого типа операции."""
    # Создаём кошелек
    resp = client.post("/api/v1/wallets")
    wallet_uuid = resp.json()["uuid"]

    # Пытаемся выполнить несуществующую операцию
    resp = client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "INVALID", "amount": 100}
    )
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Invalid operation type"


def test_wallet_not_found(client):
    """Тест несуществующего кошелька."""
    # Случайный UUID
    import uuid
    random_uuid = str(uuid.uuid4())

    # Получение несуществующего кошелька
    resp = client.get(f"/api/v1/wallets/{random_uuid}")
    assert resp.status_code == 404

    # Операция с несуществующим кошельком
    resp = client.post(
        f"/api/v1/wallets/{random_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": 100}
    )
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Wallet not found"
