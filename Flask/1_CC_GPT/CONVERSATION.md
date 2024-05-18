# ChatGPT conversation: 1_CC_GPT #

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

## ChatGPT response: ##
To implement token revocation using Redis, you can create a middleware function that checks if the token is revoked before allowing access to protected routes. Here's how you can modify your code to include token revocation:

```python
from datetime import timedelta
import redis

from flask import Flask, jsonify
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager

ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.route("/login", methods=["POST"])
def login():
    access_token = create_access_token(identity="example_user")
    return jsonify(access_token=access_token)

# Middleware to check token revocation
@jwt.token_in_blacklist_loader
def check_if_token_revoked(decrypted_token):
    jti = decrypted_token["jti"]
    token_revoked = redis_client.get(jti)
    return token_revoked is not None

# A blocklisted access token will not be able to access this any more
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(hello="world")

# Logout route to revoke tokens
@app.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    redis_client.set(jti, "true", ex=ACCESS_EXPIRES)
    return jsonify(msg="Successfully logged out")

if __name__ == "__main__":
    app.run()
```

In this code:

- We've added a Redis connection using the `redis` library.
- A middleware function `check_if_token_revoked` is added using `@jwt.token_in_blacklist_loader`. This function checks if the token has been revoked by checking if its JTI (JWT ID) exists in the Redis database.
- A `/logout` route is added to revoke tokens. When a user logs out, their JWT ID is stored in Redis with an expiration time equal to the token expiration time. This effectively revokes the token.