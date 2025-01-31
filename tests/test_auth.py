from unittest.mock import patch

import jwt
import pytest

from fastapi_oidc_auth.auth import OpenIDConnectException


def test_oidc_init(mock_oidc):
    """Test OpenIDConnect initialization."""
    assert mock_oidc.issuer == "https://example.com/auth/realms/test"
    assert mock_oidc.authorization_endpoint == "https://example.com/auth"


def test_get_auth_redirect_uri(mock_oidc):
    """Test generating authentication redirect URI."""
    redirect_uri = "https://myapp.com/callback"
    auth_uri = mock_oidc.get_auth_redirect_uri(redirect_uri)
    assert "response_type=code" in auth_uri
    assert "client_id=test-client" in auth_uri
    assert "redirect_uri=https%3A%2F%2Fmyapp.com%2Fcallback" in auth_uri


@pytest.mark.usefixtures("mock_requests_post")
def test_get_auth_token(mock_oidc, mock_requests_post):
    """Test retrieving an authentication token."""
    token = mock_oidc.get_auth_token("test-code", "https://myapp.com/callback")
    assert "access_token" in token
    assert "id_token" in token


@pytest.mark.usefixtures("mock_requests_post")
def test_authenticate_hs256(mock_oidc, mock_requests_post):
    """Test authentication with HS256-signed ID token."""
    with patch("jwt.get_unverified_header", return_value={"alg": "HS256"}):
        user_info = mock_oidc.authenticate(
            "test-code", "https://myapp.com/callback"
        )
        assert user_info["sub"] == "123"


def test_authenticate_invalid_token(mock_oidc):
    """Test authentication with an invalid token."""
    with patch("jwt.get_unverified_header", side_effect=jwt.DecodeError):
        with pytest.raises(OpenIDConnectException):
            mock_oidc.authenticate(
                "invalid-code", "https://myapp.com/callback"
            )


def test_validate_sub_matching_success(mock_oidc, mock_jwt):
    """Test subject (sub) matching."""
    mock_oidc.validate_sub_matching(mock_jwt, mock_jwt)  # Should not raise


def test_validate_sub_matching_failure(mock_oidc, mock_jwt):
    """Test subject (sub) mismatch error."""
    user_info = {**mock_jwt, "sub": "wrong-sub"}
    with pytest.raises(OpenIDConnectException, match="Subject mismatch error"):
        mock_oidc.validate_sub_matching(mock_jwt, user_info)


@pytest.mark.usefixtures("mock_requests_post")
def test_obtain_validated_token_hs256(mock_oidc, mock_requests_post):
    """Test validating a HS256 token."""
    # Create a valid mock JWT token with the required "aud" claim
    payload = {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": 1516239022,
        "aud": "test-client",
    }
    secret = "test-secret"
    mock_token = jwt.encode(payload, secret, algorithm="HS256")

    with patch("jwt.get_unverified_header", return_value={"alg": "HS256"}):
        with patch.object(
            mock_oidc, "client_secret", secret
        ):  # Ensure correct secret is used
            with patch.object(
                mock_oidc, "client_id", "test-client"
            ):  # <-- Ensure client_id matches aud
                token = mock_oidc.obtain_validated_token("HS256", mock_token)

    assert token["sub"] == "1234567890"
    assert token["name"] == "John Doe"


@pytest.mark.usefixtures("mock_requests_post")
def test_obtain_validated_token_invalid(mock_oidc):
    """Test validating a token with an unsupported algorithm."""
    with pytest.raises(
        OpenIDConnectException, match="Unsupported jwt algorithm found."
    ):
        mock_oidc.obtain_validated_token("unknown_alg", "mock-token")
