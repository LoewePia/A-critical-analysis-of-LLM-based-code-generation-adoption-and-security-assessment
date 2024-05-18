```python
from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'password1'),
    User(2, 'user2', 'password2'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


# Function to authenticate users
def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


# Function to identity users
def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

jwt = JWT(app, authenticate, identity)


# Protected endpoint
@app.route('/protected')
@jwt_required()
def protected():
    return jsonify({"asdf": "sadf"}), 200


# Public endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user = authenticate(username, password)

    if user:
        access_token = jwt.jwt_encode_callback(user).decode('utf-8')
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


if __name__ == '__main__':
    app.run(debug=True)
```
