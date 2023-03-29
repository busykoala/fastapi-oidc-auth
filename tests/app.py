from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse
import uvicorn

from fastapi_oidc_auth.auth import OpenIDConnect

host = "http://localhost:8080"
realm = "myrealm"
client_id = "myclient"
client_secret = "mBSW6roRlpoHp0bbGEAQIqUmaNZ4VDqd"
app_uri = "http://localhost:5000"

oidc = OpenIDConnect(host, realm, app_uri, client_id, client_secret)
app = FastAPI()


@app.get("/")
async def homepage(request: Request) -> dict[str, str]:
    return {"message": "Not a secret"}


@app.get("/secret")
@oidc.require_login
async def secret(request: Request) -> dict[str, str]:
    return {"message": "Secret"}


@app.get("/login")
@oidc.require_login
async def login(request: Request) -> dict[str, str]:
    return {"message": "success", "user_info": request["user_info"]}


@app.get("/logout")
async def logout(request: Request) -> RedirectResponse:
    return oidc.logout(request=request)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
