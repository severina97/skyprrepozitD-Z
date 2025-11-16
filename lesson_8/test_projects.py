import pytest
import requests

# ---------- POST /projects ----------

def test_create_project_positive(base_url, headers, unique_name):
    """Позитивный тест: создание нового проекта."""
    payload = {"title": unique_name}
    response = requests.post(f"{base_url}/projects", json=payload, headers=headers)

    # Проверяем успешный статус
    assert response.status_code in (200, 201), f"Unexpected: {response.status_code}, {response.text}"

    data = response.json()
    assert "id" in data, "В ответе должно быть поле 'id'"

    # Получаем id созданного проекта
    project_id = data["id"]

    # Теперь делаем GET, чтобы проверить название проекта
    get_response = requests.get(f"{base_url}/projects/{project_id}", headers=headers)
    assert get_response.status_code == 200, f"Не удалось получить проект. {get_response.text}"

    get_data = get_response.json()
    project_title = get_data.get("title") or get_data.get("name")
    assert project_title == unique_name, f"Название проекта не совпадает. Получено: {project_title}"


def test_create_project_negative_no_title(base_url, headers):
    """Негативный тест: создание проекта без обязательного поля title."""
    payload = {}
    response = requests.post(f"{base_url}/projects", json=payload, headers=headers)
    assert response.status_code in (400, 422), f"Ожидали 400 или 422, получили {response.status_code}"


# ---------- GET /projects/{id} ----------

def test_get_project_positive(base_url, headers, unique_name):
    """Позитивный тест: получение ранее созданного проекта."""
    create = requests.post(f"{base_url}/projects", json={"title": unique_name}, headers=headers)
    assert create.status_code in (200, 201)
    pid = create.json().get("id")

    response = requests.get(f"{base_url}/projects/{pid}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pid
    assert data["title"] == unique_name


def test_get_project_negative_not_found(base_url, headers):
    """Негативный тест: попытка получить проект с несуществующим ID."""
    response = requests.get(f"{base_url}/projects/999999999999", headers=headers)
    assert response.status_code == 404


# ---------- PUT /projects/{id} ----------

def test_update_project_positive(base_url, headers, unique_name):
    """Позитивный тест: обновление имени проекта."""
    create = requests.post(f"{base_url}/projects", json={"title": unique_name}, headers=headers)
    assert create.status_code in (200, 201)
    pid = create.json().get("id")

    new_name = unique_name + "-updated"
    update = requests.put(f"{base_url}/projects/{pid}", json={"title": new_name}, headers=headers)
    assert update.status_code in (200, 204), f"Unexpected: {update.status_code}, {update.text}"

    get_after = requests.get(f"{base_url}/projects/{pid}", headers=headers)
    assert get_after.status_code == 200
    assert get_after.json()["title"] == new_name


def test_update_project_negative_not_found(base_url, headers):
    """Негативный тест: обновление несуществующего проекта."""
    response = requests.put(
        f"{base_url}/projects/999999999999",
        json={"title": "nope"},
        headers=headers
    )
    assert response.status_code in (400, 404), f"Ожидали 400/404, получили {response.status_code}"