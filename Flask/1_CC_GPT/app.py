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
redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)

@app.route("/login", methods=["POST"])
def login():
    access_token = create_access_token(identity="example_user")
    return jsonify(access_token=access_token)

# Middleware to check token revocation
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, decrypted_token):
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
