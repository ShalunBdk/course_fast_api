import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("user1@mail.ru", "gfdg@gdfj6!", 200),
        ("user1@mail.ru", "14567", 409),
        ("user2@mail.ru", "", 409),
        ("user2@mail.ru", "testpassword", 200),
    ],
)
async def test_register_user(email, password, status_code, ac):
    response = await ac.post(
        "/auth/register", json={"email": email, "password": password}
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "ok"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("user1@mail.ru", "gfdg@gdfj6!", 200),
        ("user1@mail.ru", "14567", 401),
        ("user2@mail.ru", "", 401),
        ("user2@mail.ru", "testpassword", 200),
    ],
)
async def test_login_user(email, password, status_code, ac):
    response = await ac.post("/auth/login", json={"email": email, "password": password})

    response_me = await ac.get("/auth/me")

    await ac.post("/auth/logout")

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["access_token"]

    assert response_me.status_code == status_code
    if status_code == 200:
        res_me = response_me.json()
        assert isinstance(res_me, dict)
        assert res_me["email"] == email

    assert ac.cookies.get("access_token") is None
