from fastapi import FastAPI, Request

from fastapi_oidc_auth.auth import OpenIDConnect

host = "http://localhost:8080"
realm = "myrealm"
client_id = "myclient"
client_secret = "mBSW6roRlpoHp0bbGEAQIqUmaNZ4VDqd"
app_uri = "http://localhost:5000"

oidc = OpenIDConnect(host, realm, app_uri, client_id, client_secret)
app = FastAPI()


@app.get("/very-secret")
@oidc.require_login
async def very_secret(request: Request) -> dict[str, str]:
    return {"message": " success", "user_info": request.user_info}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
