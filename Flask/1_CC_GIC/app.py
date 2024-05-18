from datetime import timedelta
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    create_access_token, get_jwt, jwt_required, JWTManager
)
import redis

ACCESS_EXPIRES = timedelta(hours=1)
#BLOCKLIST = set()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

# Setup redis instance
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = r.get(jti)
    return token_in_redis is not None

'''@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    return {
        "jti": get_jwt()["jti"],
    }'''

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