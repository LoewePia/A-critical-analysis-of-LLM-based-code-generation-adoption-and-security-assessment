from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'

# Mock user data (replace with a real database in production)
users = {
    'user1': {
        'id': 1,
        'username': 'user1',
        'password': 'password1'
    },
    'user2': {
        'id': 2,
        'username': 'user2',
        'password': 'password2'
    }
}

# Function to authenticate users
def authenticate(username, password):
    user = users.get(username, None)
    if user and safe_str_cmp(user['password'].encode('utf-8'), password.encode('utf-8')):
        return user

# Function to identity users
def identity(payload):
    user_id = payload['identity']
    return users.get(user_id, None)

jwt = JWT(app, authenticate, identity)

# Protected endpoint
@app.route('/protected')
@jwt_required()
def protected():
    return jsonify(logged_in_as=current_identity['username']), 200

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
        access_token = jwt.jwt_encode_callback(user)
        return jsonify({'access_token': access_token.decode('utf-8')}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
