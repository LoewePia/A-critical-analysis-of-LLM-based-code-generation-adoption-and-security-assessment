# GitHub Copilot conversation: 2_CC_GIC #
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

## GitHub Copilot response: ##
First, we will create a custom decorator `admin_required` that will check if the user is an admin. We will add an additional claim `is_admin` to the JWT token. If the claim is not present or if it's false, the decorator will return a 403 Forbidden error. Then, we will use this decorator on the protected endpoint.

Here is the updated code:

```python
from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from flask_jwt_extended import JWTManager

app =

 Flask

(__name__)

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
```

In the `/login` endpoint, I've added a simple username and password check. If the username is 'admin' and the password is 'password', it will create a token with the `is_admin` claim set to True. Otherwise, it will return a 401 Unauthorized error. You should replace this with your own authentication logic.