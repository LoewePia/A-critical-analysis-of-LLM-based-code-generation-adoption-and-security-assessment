# GitHub Copilot conversation: 3_EC_GIC #
## Prompt: ##
I get this error:
```
ERROR in app: Exception on /admin/protected [GET]
Traceback (most recent call last):
  File "/opt/anaconda3/lib/python3.8/site-packages/flask/app.py", line 1473, in wsgi_app
    response = self.full_dispatch_request()
  File "/opt/anaconda3/lib/python3.8/site-packages/flask/app.py", line 882, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/opt/anaconda3/lib/python3.8/site-packages/flask/app.py", line 880, in full_dispatch_request
    rv = self.dispatch_request()
  File "/opt/anaconda3/lib/python3.8/site-packages/flask/app.py", line 865, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
  File "/Users/pia.loewe/Documents/ChatGPT/first_conv/3_EC_GPT/server/app/admin/views.py", line 14, in protected
    current_user = get_jwt_identity()
  File "/opt/anaconda3/lib/python3.8/site-packages/flask_jwt_extended/utils.py", line 63, in get_jwt_identity
    return get_jwt().get(config.identity_claim_key, None)
  File "/opt/anaconda3/lib/python3.8/site-packages/flask_jwt_extended/utils.py", line 29, in get_jwt
    raise RuntimeError(
RuntimeError: You must call `@jwt_required()` or `verify_jwt_in_request()` before using this method
127.0.0.1 - - [20/Apr/2024 22:20:01] "GET /admin/protected HTTP/1.1" 500 -
```
Fix it:
```python
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from . import admin
from flask import Flask, jsonify, request

users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'}
}

# file: server/app/admin/views.py
@jwt_required()
@admin.route('/protected', methods=['GET'])
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@admin.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    if username not in users or users[username]['password'] != password:
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

```

## GitHub Copilot response: ##
The error message indicates that you're trying to use `get_jwt_identity()` without first verifying the JWT token. This is usually done by calling `@jwt_required()` before the route that uses `get_jwt_identity()`.

However, in your code, you're using `@jwt_required()` after `@admin.route()`. The order of decorators in Flask matters. The `@jwt_required()` decorator should be applied first. Here's the corrected code:

```python
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from . import admin
from flask import Flask, jsonify, request

users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'}
}

# file: server/app/admin/views.py
@admin.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@admin.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    if username not in users or users[username]['password'] != password:
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
```

This should solve the issue. The `@jwt_required()` decorator will now be applied before the route is defined, ensuring that the JWT token is verified before `get_jwt_identity()` is called.