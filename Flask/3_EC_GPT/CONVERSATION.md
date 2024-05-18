# ChatGPT conversation: 3_EC_GPT #
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

## ChatGPT response: ##
The error you're encountering indicates that the `@jwt_required()` decorator is not being properly invoked before accessing the `get_jwt_identity()` function in your `protected` endpoint. To fix this, make sure that the `@jwt_required()` decorator is used to protect the route where you're calling `get_jwt_identity()`.

Here's the corrected version of your code:

```python
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from . import admin
from flask import jsonify, request

users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'}
}

# file: server/app/admin/views.py
@admin.route('/protected', methods=['GET'])
@jwt_required()  # Move the decorator here to protect the route
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

By moving the `@jwt_required()` decorator to be above the `protected` function definition, you ensure that it is called before the `protected` endpoint is accessed, thus resolving the error.