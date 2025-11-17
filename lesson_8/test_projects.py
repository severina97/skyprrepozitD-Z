import pytest
import requests
import os
import uuid


# ---------------- FIXTURES ----------------

@pytest.fixture(scope="session")
def base_url() -> str:
    """Базовый URL API YouGile."""
    return "https://ru.yougile.com/api-v2"


@pytest.fixture(scope="session")
def api_key() -> str:
    """Получение API-ключа. Если не задан — бросаем исключение."""
    key = os.getenv("YOUGILE_API_KEY")
    if not key:
        raise RuntimeError("Не задан YOUGILE_API_KEY в переменных окружения!")
    return key


@pytest.fixture(scope="session")
def headers(api_key: str) -> dict:
    """Формирование заголовков авторизации."""
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


@pytest.fixture()
def unique_name() -> str:
    """Генерация уникального имени проекта."""
    return "pytest-project-" + uuid.uuid4().hex[:8]


# ---------------- TESTS ----------------

def test_create_project_positive(base_url: str, headers: dict, unique_name: str):
    """Позитивный тест: создание нового проекта."""
    payload = {"title": unique_name}
    response = requests.post(f"{base_url}/projects", json=payload, headers=headers)

    # Строгая проверка статуса
    assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}: {response.text}"

    data = response.json()

    # Проверяем наличие id
    assert "id" in data, "В ответе должно быть поле id"
    pid = data["id"]

    # Проверяем название через GET (POST иногда не отдаёт title)
    get_response = requests.get(f"{base_url}/projects/{pid}", headers=headers)
    assert get_response.status_code == 200, f"GET должен вернуть 200, получил {get_response.status_code}"

    title_from_server = get_response.json().get("title", "wrong_title")
    assert title_from_server == unique_name, f"Название проекта не совпадает: {title_from_server}"


def test_create_project_negative_no_title(base_url: str, headers: dict):
    """Негативный тест: создание проекта без обязательного title."""
    payload = {}
    response = requests.post(f"{base_url}/projects", json=payload, headers=headers)

    # Строгий ожидаемый статус (у YouGile — 400)
    assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"


def test_get_project_positive(base_url: str, headers: dict, unique_name: str):
    """Позитивный тест: получение существующего проекта."""
    create_resp = requests.post(f"{base_url}/projects", json={"title": unique_name}, headers=headers)
    assert create_resp.status_code == 201, f"Ожидали 201, получили {create_resp.status_code}"

    pid = create_resp.json().get("id")
    assert pid is not None, "POST должен вернуть id"

    get_resp = requests.get(f"{base_url}/projects/{pid}", headers=headers)
    assert get_resp.status_code == 200, f"Ожидали 200, получили {get_resp.status_code}"

    title = get_resp.json().get("title", "wrong_title")
    assert title == unique_name, f"Название не совпадает: {title}"


def test_get_project_negative_not_found(base_url: str, headers: dict):
    """Негативный тест: получение несуществующего проекта."""
    response = requests.get(f"{base_url}/projects/999999999999", headers=headers)
    assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}"


def test_update_project_positive(base_url: str, headers: dict, unique_name: str):
    """Позитивный тест: обновление проекта."""
    create_resp = requests.post(f"{base_url}/projects", json={"title": unique_name}, headers=headers)
    assert create_resp.status_code == 201

    pid = create_resp.json().get("id")
    assert pid is not None, "POST должен вернуть id"

    new_name = unique_name + "-updated"
    upd_resp = requests.put(f"{base_url}/projects/{pid}", json={"title": new_name}, headers=headers)

    assert upd_resp.status_code in (200, 204), \
    f"Ожидали 200 или 204, получили {upd_resp.status_code}"

    # Проверяем результат через GET
    get_after = requests.get(f"{base_url}/projects/{pid}", headers=headers)
    assert get_after.status_code == 200

    title = get_after.json().get("title", "wrong_title")
    assert title == new_name, f"Название после обновления некорректно: {title}"


def test_update_project_negative_not_found(base_url: str, headers: dict):
    """Негативный тест: обновление несуществующего проекта."""
    response = requests.put(f"{base_url}/projects/123456789000", json={"title": "nope"}, headers=headers)
    assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}"