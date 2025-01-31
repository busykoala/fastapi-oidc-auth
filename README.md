# OpenID Connect for FastAPI

`fastapi-oidc-auth` is an extension to [FastAPI](https://fastapi.tiangolo.com/)
that allows you to add OpenID Connect based authentication for your endpoints
within minutes.

## Installation

```
# TODO: not yet released
poetry add fastapi-oidc-auth
```

## How to use

The package provides a simple decorator `@oidc.login_required` to protect
an endpoint. You can retrieve the user info directly from the request object.

```py
from typing import Dict

from fastapi import FastAPI
from fastapi import Request

from fastapi_oidc_auth.auth import OpenIDConnect

# realm (e.g. Keycloak instance)
host = "http://localhost:8080"
realm = "example-realm"
client_id = "example-client"
client_secret = "xxx765cd-20ba-44a3-9584-784807a36906"
app_uri = "http://localhost:5000"

oidc = OpenIDConnect(host, realm, app_uri, client_id, client_secret)
app = FastAPI()


@app.get("/very-secret")
@oidc.require_login
async def very_secret(request: Request) -> Dict:
    return {"message": "success", "user_info": request.user_info}
```

## Ongoing Work

- Maybe release package
- Possibly refactor to a more FastAPIish style (middleware/depends)
- Make more configurable

## Develompent

```bash
poetry install

# Run tests
poetry run pytest

# Run linter
poetry run ruff format
poetry run ruff check --fix
```
