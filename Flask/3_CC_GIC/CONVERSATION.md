# GitHub Copilot conversation: 3_CC_GIC #
## Prompt: ##
Complement this piece of code to check the issuer of the JWT whenever the JWT is used:

```python
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random, secure key in production
jwt = JWTManager(app)

class User(object):
    def __init__(self, id, firstname, lastname, username, password):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.languages = []

    def get_languages(self):
        return self.languages


# Mock data
users = [User(1, "Joe", "Vanijs", "joev", "lekkerijs2"),
         User(2, "Tom", "Indesneeuw", "tomsneeuw", "winter"),
         User(3, "Lena", "Klasvogel", "lenakv", "amsel")]

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "No JSON in request."}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "No username or password was given"}), 400

    for user in users:
        if user.username == username and user.password == password:
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200

    return jsonify({"msg": "The username or password is not correct"}), 401


# Protected endpoint
@app.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    user_now = get_jwt_identity()
    return jsonify(logged_in_as=user_now), 200


@app.route('/languages', methods=['POST'])
@jwt_required()
def add_language():
    if not request.is_json:
        return jsonify({"msg": "No JSON in request."}), 400

    language = request.json.get('language')

    user_now = get_jwt_identity()
    for user in users:
        if user.username == user_now:
            user.get_languages().append(language)
            return '', 204

@app.route('/languages', methods=['GET'])
@jwt_required()
def get_languages():
    user_now = get_jwt_identity()
    for user in users:
        if user.username == user_now:
            return jsonify(languages=user.get_languages())


if __name__ == '__main__':
    app.run(debug=True)
```

## GitHub Copilot response: ##
To check the issuer of the JWT, you can add a custom claim to the JWT when it's created and then verify that claim whenever the JWT is used. Here's how you can do it:

1. Add a custom claim named 'iss' (short for issuer) to the JWT when it's created. You can do this by modifying the `login` function.

2. Verify the 'iss' claim in a custom decorator that you can use to protect your endpoints. This decorator will first call `jwt_required()` to ensure that a valid JWT is present, and then it will check the 'iss' claim.

Here's the modified code:

```python
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random, secure key in production
jwt = JWTManager(app)

ISSUER = 'my-app'  # Change this to your app's name

class User(object):
    # ... rest of your User class ...

# ... rest of your code ...

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    # ... rest of your login code ...

    for user in users:
        if user.username == username and user.password == password:
            # Add 'iss' claim to JWT
            additional_claims = {'iss': ISSUER}
            access_token = create_access_token(identity=username, additional_claims=additional_claims)
            return jsonify(access_token=access_token), 200

    return jsonify({"msg": "The username or password is not correct"}), 401

# Custom decorator to check JWT issuer
def jwt_required_and_check_issuer():
    def wrapper(fn):
        @jwt_required()
        @functools.wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims['iss'] != ISSUER:
                return jsonify({"msg": "Invalid JWT issuer"}), 401
            else:
                return fn(*args, **kwargs)
        return decorator
    return wrapper

# Protected endpoint
@app.route('/user', methods=['GET'])
@jwt_required_and_check_issuer()
def get_user():
    # ... rest of your get_user code ...

# ... rest of your code ...
```

In this code, `jwt_required_and_check_issuer` is a custom decorator that first calls `jwt_required()` to ensure that a valid JWT is present, and then checks the 'iss' claim. If the 'iss' claim doesn't match the expected issuer, it returns a 401 response. Otherwise, it calls the original function.