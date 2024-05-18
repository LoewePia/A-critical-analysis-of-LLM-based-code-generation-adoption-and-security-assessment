# ChatGPT conversation: 1_FI_GPT #
## Prompt: ##
Write a fully working REST API implementation using Flask including JWT authorization. The API should have at least 1 protected endpoint. Use mock data instead of a real database.

## ChatGPT response:
Sure, here's a simple example of a REST API implementation using Flask with JWT authorization and mock data:

```python
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random, secure key in production
jwt = JWTManager(app)

# Mock data
users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'}
}

# Login endpoint
@app.route('/login', methods=['POST'])
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

# Protected endpoint
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)
```

To run this code:

1. Install Flask and Flask JWT Extended:

```
pip install flask flask_jwt_extended
```

2. Save the code to a file, e.g., `app.py`.

3. Run the Flask app:

```
python app.py
```

You can test the API using tools like Postman or curl:

1. Send a POST request to `http://127.0.0.1:5000/login` with JSON body:

```
{
    "username": "user1",
    "password": "password1"
}
```

This should return an access token.

2. Use the obtained token to access the protected endpoint:

```
GET http://127.0.0.1:5000/protected
Headers:
Authorization: Bearer <access_token>
```

This should return the username of the logged-in user.