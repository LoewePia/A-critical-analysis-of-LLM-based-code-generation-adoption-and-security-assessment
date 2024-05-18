# GitHub Copilot conversation: 1_CC_GPT #

## Prompt: ##
Complement this piece of code with a token revocation mechanism using Redis:
```python from datetime import timedelta
from flask import Flask
from flask import jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    access_token = create_access_token(identity="example_user")
    return jsonify(access_token=access_token)

# A blocklisted access token will not be able to access this any more
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(hello="world")


if __name__ == "__main__":
    app.run()
```

## GitHub Copilot response: ##
To add a token revocation mechanism using Redis, you need to do the following:

1. Install the `flask_jwt_extended` and `redis` libraries.
2. Create a Redis instance and connect it to your Redis server.
3. Add a callback function to store the JWT tokens in Redis when they are created.
4. Add a callback function to check if a JWT token is in Redis when a protected route is accessed.
5. Add a route to revoke a token by adding it to the blocklist in Redis.

Here is the updated code:

```python
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    create_access_token, get_jwt, jwt_required, JWTManager
)
import redis

ACCESS_EXPIRES = timedelta(hours=1)
BLOCKLIST = set()

app

 =

 Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

# Setup redis instance
r = redis.Redis(host='localhost', port=6379, db=0)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = r.get(jti)
    return token_in_redis is not None

@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    return {
        "jti": get_jwt()["jti"],
    }

@app.route("/login", methods=["POST"])
def login():
    access_token = create_access_token(identity="example_user")
    return jsonify(access_token=access_token)

@app.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    r.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(hello="world")

if __name__ == "__main__":
    app.run()
```

1 vulnerability:
- hardcoded-credentials Embedding credentials in source code risks unauthorized access

This code will add the JWT token identifier (jti) to the access token when it is created. When a token is checked, it will look in Redis to see if the jti is present. If it is, the token is considered blocklisted and will not grant access. The `/logout` route will add the jti of the current token to Redis, effectively revoking it.