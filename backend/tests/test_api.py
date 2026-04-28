import pytest
from fastapi.testclient import TestClient
from app.main import app, _rate_limit_store

client = TestClient(app)


class TestQueryStock:
    def test_missing_params(self):
        response = client.get("/api/stock/query")
        assert response.status_code == 422

    def test_rate_limit(self):
        _rate_limit_store.clear()
        ip = "127.0.0.1"
        for i in range(5):
            response = client.get(
                "/api/stock/query",
                params={"stock_code": "000001"},
                headers={"X-Forwarded-For": ip}
            )
        response = client.get(
            "/api/stock/query",
            params={"stock_code": "000001"},
            headers={"X-Forwarded-For": ip}
        )
        assert response.status_code == 429

    def test_invalid_stock(self, monkeypatch):
        _rate_limit_store.clear()

        def mock_fetch(*args, **kwargs):
            raise ValueError("no data")

        import app.data_service
        monkeypatch.setattr(app.data_service, "fetch_stock_data", mock_fetch)
        response = client.get("/api/stock/query", params={"stock_code": "999999"})
        assert response.status_code == 404
