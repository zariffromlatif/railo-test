import os
import sqlite3
import pytest
from unittest.mock import patch, MagicMock
from app import app, get_db, BASE_DIR


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db():
    """Creates an in-memory SQLite database for testing."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, role TEXT, email TEXT)"
    )
    conn.execute(
        "INSERT INTO users (id, username, role, email) VALUES (1, 'alice', 'admin', 'alice@example.com')"
    )
    conn.execute(
        "INSERT INTO users (id, username, role, email) VALUES (2, 'bob', 'user', 'bob@example.com')"
    )
    conn.commit()
    return conn


class TestDownloadEndpoint:
    """Tests for the /download endpoint."""

    def test_download_normal_file(self, client):
        """A normal filename request should reach send_file with the correct path."""
        with patch("app.send_file") as mock_send:
            mock_send.return_value = "OK"
            client.get("/download?file=report.pdf")
            called_path = mock_send.call_args[0][0]
            assert "report.pdf" in called_path


class TestUserEndpoint:
    """Tests for the /user endpoint."""

    def test_get_existing_user(self, client, mock_db):
        """Looking up an existing user by email should return their data."""
        with patch("app.get_db", return_value=mock_db):
            response = client.get("/user?email=alice@example.com")
            data = response.get_json()
            assert response.status_code == 200
            assert data["username"] == "alice"
            assert data["role"] == "admin"

    def test_get_nonexistent_user(self, client, mock_db):
        """Looking up a non-existent email should return 404."""
        with patch("app.get_db", return_value=mock_db):
            response = client.get("/user?email=nobody@example.com")
            assert response.status_code == 404

    def test_get_second_user(self, client, mock_db):
        """Looking up the second user should return their data."""
        with patch("app.get_db", return_value=mock_db):
            response = client.get("/user?email=bob@example.com")
            data = response.get_json()
            assert response.status_code == 200
            assert data["username"] == "bob"


class TestPingEndpoint:
    """Tests for the /ping endpoint."""

    def test_ping_normal_host(self, client):
        """A normal hostname should produce output."""
        with patch("os.popen") as mock_popen:
            mock_popen.return_value = MagicMock(read=MagicMock(return_value="PING OK"))
            response = client.get("/ping?host=8.8.8.8")
            data = response.get_json()
            assert "output" in data

    def test_ping_returns_200(self, client):
        """The ping endpoint should return a 200 status."""
        with patch("os.popen") as mock_popen:
            mock_popen.return_value = MagicMock(
                read=MagicMock(return_value="PONG")
            )
            response = client.get("/ping?host=localhost")
            assert response.status_code == 200


class TestChargeEndpoint:
    """Tests for the /charge endpoint."""

    def test_charge_returns_key_prefix(self, client):
        """The charge endpoint should return a key_prefix field."""
        response = client.get("/charge")
        data = response.get_json()
        assert "key_prefix" in data
        assert isinstance(data["key_prefix"], str)

    def test_charge_returns_200(self, client):
        """The charge endpoint should always return 200."""
        response = client.get("/charge")
        assert response.status_code == 200
