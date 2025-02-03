import pytest

from fastapi_oidc_auth.exceptions import OpenIDConnectException


def test_openid_connect_exception():
    """Test OpenIDConnectException behavior."""
    with pytest.raises(OpenIDConnectException, match="Authentication failed"):
        raise OpenIDConnectException("Authentication failed")
