API_KEY_HEADER = {"X-Api-Key": "test-api-key"}

def test_health_ok_200(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
