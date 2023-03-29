# OpenID Connect for FastAPI

`prokie-fastapi-oidc-auth` is an extension to
[FastAPI](https://fastapi.tiangolo.com/) that allows you to add OpenID
Connect based authentication for your endpoints within minutes.

## Installation

```
pip install prokie-fastapi-oidc-auth
```

## Keycloak settings

### Admin

```
admin_username = "admin"
admin_password = "admin"
host = "http://localhost:8080"
```

### Realm

```
realm = "myrealm"
```

### Client

Set the `Access Type` to `confidential` and `Standard Flow Enabled` to
`ON`. Make sure that `Valid Redirect URIs` contain the URI of your app
or `*` if you want to allow all URIs. Make sure `Client Protocol` is set
to `openid-connect`.

```
client = "myclient"
secret = "xZEIb4wGoWseNumHJ4Vb7pYvdX3SIQeg"
```

### User

```
user_username = "myuser"
user_password = "myuser"
```

## How to use

See test.py for a complete example.

## Testing

To start a Keycloak instance for testing, run the following command:

```
docker run -d -p 8080:8080 \
            -e KEYCLOAK_USER=admin \
            -e KEYCLOAK_PASSWORD=admin \
            -e KEYCLOAK_IMPORT=/opt/jboss/keycloak/imports/realm-export.json \
            -v $(pwd)/realm-export.json:/opt/jboss/keycloak/imports/realm-export.json \
            --name keycloak \
            jboss/keycloak:16.1.1
```

To export the realm configuration, run the following command:

```
docker exec -it keycloak /opt/jboss/keycloak/bin/standalone.sh \
-Djboss.socket.binding.port-offset=100 -Dkeycloak.migration.action=export \
-Dkeycloak.migration.provider=singleFile \
-Dkeycloak.migration.realmName=myrealm \
-Dkeycloak.migration.usersExportStrategy=REALM_FILE \
-Dkeycloak.migration.file=/tmp/realm-export.json
```
