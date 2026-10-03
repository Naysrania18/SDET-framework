import pytest

pytestmark = pytest.mark.api

REQUIRED_USER_FIELDS = {"id", "name", "username", "email", "address", "phone"}


@pytest.mark.smoke
def test_get_users_returns_200_and_ten_users(api):
    resp = api.get("/users")
    assert resp.status_code == 200
    assert len(resp.json()) == 10


@pytest.mark.parametrize("user_id", [1, 5, 10])
def test_get_user_has_required_schema(api, user_id):
    body = api.get(f"/users/{user_id}").json()
    assert REQUIRED_USER_FIELDS <= body.keys()
    assert body["id"] == user_id
    assert "@" in body["email"]


@pytest.mark.parametrize("user_id", [0, 9999])
def test_get_unknown_user_returns_404(api, user_id):  # negative test
    assert api.get(f"/users/{user_id}").status_code == 404


def test_create_post_returns_201_and_echoes_payload(api):
    payload = {"title": "sdet demo", "body": "hello", "userId": 1}
    resp = api.post("/posts", json=payload)
    assert resp.status_code == 201
    assert resp.json()["title"] == payload["title"]
    assert "id" in resp.json()


def test_response_time_under_two_seconds(api):  # basic non-functional check
    assert api.get("/users/1").elapsed.total_seconds() < 2
