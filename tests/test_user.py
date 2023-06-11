from conftest import async_session_test, client


def test_create_user():
    response = client.post("/v1/user/", json={
        "name": "vlad",
        "surname": "vlad",
        "patronymic": "vlad",
        "type_user": 1,
        "login": "vlad",
        "password": "vlad"
    })
    assert response.status_code == 201


def test_get_user():
    payload = f"grant_type=&username=vlad&password=vlad&client_id=&client_secret="
    response = client.post("/v1/login/sign-in/", json=payload, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    })
    token = response.json()['access_token']
    response = client.get("/v1/user/1", headers={
          "Authorization": f"Bearer {token}"
    })
    assert response.json() == {
        "id": 1,
        "is_activ": False,
        "name": "vlad",
        "surname": "vlad",
        "patronymic": "vlad",
        "type_user": 1,
        "login": "vlad"
    }