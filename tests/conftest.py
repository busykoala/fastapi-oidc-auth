from unittest.mock import MagicMock
from unittest.mock import patch

import jwt
import pytest

from fastapi_oidc_auth.auth import OpenIDConnect


@pytest.fixture
def mock_well_known_config():
    return {
        "issuer": "https://example.com/auth/realms/test",
        "authorization_endpoint": "https://example.com/auth",
        "token_endpoint": "https://example.com/token",
        "jwks_uri": "https://example.com/jwks",
    }


@pytest.fixture
def mock_oidc(mock_well_known_config):
    """Mock OpenIDConnect instance."""
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_well_known_config
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        return OpenIDConnect(
            host="https://example.com",
            realm="test",
            app_uri="https://myapp.com",
            client_id="test-client",
            client_secret="test-secret",
        )


@pytest.fixture
def mock_jwt():
    """Mock a decoded JWT token."""
    return {
        "sub": "1234567890",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "iat": 1710000000,
        "exp": 1710003600,
        "aud": "test-client",
    }


@pytest.fixture
def mock_requests_post():
    """Mock `requests.post` for token endpoint."""
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "mock_access_token",
            "id_token": jwt.encode(
                {"sub": "123", "aud": "test-client"},
                "test-secret",
                algorithm="HS256",
            ),
        }
        mock_post.return_value = mock_response
        yield mock_post
