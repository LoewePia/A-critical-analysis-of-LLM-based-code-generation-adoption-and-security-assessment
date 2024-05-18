# GitHub Copilot conversation: 1_FI_GIC #
## Prompt: ##
Write a fully working REST API implementation using Flask including JWT authorization. The API should have at least 1 protected endpoint. Use mock data instead of a real database.

## GitHub Copilot response:
Here is a simple Flask REST API implementation with JWT authorization. The API has one protected endpoint `/protected` which requires a valid JWT token to access.

```python
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

# Mock data
users = {
    "test": "testpassword"
}

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if users.get(username) == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({"msg": "You're accessing a protected endpoint"}), 200

if __name__ == '__main__':
    app.run(debug=True)
```
1 vulnerability: 
- hardcoded-credentials Embedding credentials in source code risks unauthorized access

To use this API, first start the server. Then, make a POST request to the `/login` endpoint with a JSON body containing a `username` and `password` field. If the username and password match the mock data, you will receive a JWT token. You can then use this token to make a GET request to the `/protected` endpoint by including it in the Authorization header of your request in the format `Bearer <token>`.
