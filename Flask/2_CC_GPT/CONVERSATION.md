# ChatGPT conversation: 2_CC_GPT #
## Prompt: ##
Can you complement this piece of code so that only admins can access the protected endpoint. Use a custom decorator and an additional claim for this:
```python
from flask import Flask
from flask import jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    access_token = create_access_token()
    return jsonify(access_token=access_token)


@app.route("/protected", methods=["GET"])
def protected():
    return jsonify(foo="bar")


if __name__ == "__main__":
    app.run()
```

## ChatGPT response: ##
Sure, you can achieve this by creating a custom decorator that checks if the user making the request is an admin. You'll need to modify the `/protected` route to use this decorator. Here's how you can do it:

```python
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
```

In this code:

- `admin_required` is a custom decorator that checks if the user is in the `admin_users` list.
- The `protected` endpoint is decorated with both `jwt_required()` from Flask JWT Extended and `admin_required` to ensure the user is authenticated and is an admin.
- Dummy data `admin_users` contains email addresses of admin users. In a real application, you would replace this with your actual admin user data.