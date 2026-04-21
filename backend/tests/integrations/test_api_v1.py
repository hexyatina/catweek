import pytest


def test_health_returns_200(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_schedule_endpoint_returns_200(client):
    response = client.get("/api/v1/schedule")
    assert response.status_code == 200


def test_schedule_empty_db_returns_empty(client):
    response = client.get("/api/v1/schedule")
    assert response.status_code == 200
    data = response.get_json()
    if isinstance(data, list):
        assert data == []
    else:
        assert data.get("data") == [] or data.get("schedule") == []


@pytest.mark.parametrize("route", [
    "/api/v1/lookup/groups",
    "/api/v1/lookup/lecturers",
    "/api/v1/lookup/venues",
])
def test_lookup_routes_return_200(client, route):
    response = client.get(route)
    assert response.status_code == 200


def test_unknown_route_returns_404(client):
    response = client.get("/api/v1/does-not-exist")
    assert response.status_code == 404


def test_missing_api_key_401(app):
    from unittest.mock import patch, MagicMock

    mock_settings = MagicMock()
    mock_settings.debug = False
    mock_settings.API_KEY = "test-api-key"

    with patch("src.app.utils.security.settings", mock_settings):
        with app.test_client() as c:
            response = c.get("/api/v1/schedule")
            assert response.status_code == 401


def test_wrong_api_key_403(app):
    from unittest.mock import patch, MagicMock

    mock_settings = MagicMock()
    mock_settings.debug = False
    mock_settings.API_KEY = "test-api-key"

    with patch("src.app.utils.security.settings", mock_settings):
        with app.test_client() as c:
            response = c.get(
                "/api/v1/schedule",
                headers={"X-Api-Key": "wrong-api-key"},
            )
        assert response.status_code == 403
