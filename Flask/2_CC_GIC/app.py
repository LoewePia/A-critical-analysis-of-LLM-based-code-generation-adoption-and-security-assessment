from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims['is_admin']:
            return fn(*args, **kwargs)
        else:
            return jsonify(msg='Admins only!'), 403
    return wrapper


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != 'admin' or password != 'password':
        return jsonify({"msg": "Bad username or password"}), 401

    additional_claims = {"is_admin": True}
    access_token = create_access_token(identity=username, additional_claims=additional_claims)
    return jsonify(access_token=access_token)


@app.route("/protected", methods=["GET"])
@admin_required
def protected():
    return jsonify(foo="bar")


if __name__ == "__main__":
    app.run()