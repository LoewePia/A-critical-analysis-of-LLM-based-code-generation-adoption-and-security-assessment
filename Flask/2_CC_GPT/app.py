from flask import Flask, jsonify, request
from functools import wraps
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Dummy data for demonstration
admin_users = ["admin@example.com"]


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user not in admin_users:
            return jsonify(message="Admins only!"), 403
        return fn(*args, **kwargs)

    return wrapper


@app.route("/login", methods=["POST"])
def login():
    # In a real scenario, you would authenticate the user and verify credentials here
    # For demonstration, just creating a dummy token
    access_token = create_access_token(identity="admin@example.com")
    return jsonify(access_token=access_token)


@app.route("/protected", methods=["GET"])
@jwt_required()
@admin_required
def protected():
    return jsonify(foo="bar")


if __name__ == "__main__":
    app.run()