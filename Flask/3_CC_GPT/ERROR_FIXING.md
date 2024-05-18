# ERROR FIXING: 3_CC_GPT #
## Prompt with error code 1: ##
I get this error:
```
[2024-05-05 13:02:00,235] ERROR in app: Exception on /check_issuer [GET]
Traceback (most recent call last):
  File "/opt/anaconda3/lib/python3.8/site-packages/flask/app.py", line 1473, in wsgi_app
    response = self.full_dispatch_request()
  File "/opt/anaconda3/lib/python3.8/site-packages/flask/app.py", line 882, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/opt/anaconda3/lib/python3.8/site-packages/flask/app.py", line 880, in full_dispatch_request
    rv = self.dispatch_request()
  File "/opt/anaconda3/lib/python3.8/site-packages/flask/app.py", line 865, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
  File "/opt/anaconda3/lib/python3.8/site-packages/flask_jwt_extended/view_decorators.py", line 170, in decorator
    return current_app.ensure_sync(fn)(*args, **kwargs)
  File "/Users/pia.loewe/Documents/ChatGPT/first_conv/3_CC_GPT/app.py", line 82, in check_issuer
    issuer = decoded_token['iss']
KeyError: 'iss' 
```
Fix it: 
```python
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token

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

# New protected endpoint to check issuer
@app.route('/check_issuer', methods=['GET'])
@jwt_required()
def check_issuer():
    jwt_token = request.headers.get('Authorization').split()[1]  # Extracting JWT token from request header
    decoded_token = decode_token(jwt_token)
    issuer = decoded_token['iss']
    return jsonify(issuer=issuer), 200

if __name__ == '__main__':
    app.run(debug=True)
```

### ChatGPT - success: ###
It seems like the JWT token might not contain the 'iss' (issuer) claim. To resolve this issue, you can first ensure that the 'iss' claim is present in your JWT token before accessing it. Here's how you can do it:

```python
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token

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

# New protected endpoint to check issuer
@app.route('/check_issuer', methods=['GET'])
@jwt_required()
def check_issuer():
    jwt_token = request.headers.get('Authorization').split()[1]  # Extracting JWT token from request header
    decoded_token = decode_token(jwt_token)
    issuer = decoded_token.get('iss')  # Use .get() to avoid KeyError if 'iss' is not present
    if issuer:
        return jsonify(issuer=issuer), 200
    else:
        return jsonify({"msg": "Issuer not found in token"}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

This modification ensures that if the 'iss' claim is not present in the JWT token, it won't raise a KeyError, and instead, it will return a message indicating that the issuer was not found in the token.

## Prompt with error code 2: ##
There is a functional error in the code, I asked you to complement a piece of code to check the issuer of the JWT whenever the JWT is used, but I can still access the endpoints without the JWT issuer being validated. Fix this:
```python
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token

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

# New protected endpoint to check issuer
@app.route('/check_issuer', methods=['GET'])
@jwt_required()
def check_issuer():
    jwt_token = request.headers.get('Authorization').split()[1]  # Extracting JWT token from request header
    decoded_token = decode_token(jwt_token)
    issuer = decoded_token.get('iss')  # Use .get() to avoid KeyError if 'iss' is not present
    if issuer:
        return jsonify(issuer=issuer), 200
    else:
        return jsonify({"msg": "Issuer not found in token"}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

### ChatGPT - success: ###
To ensure that the JWT issuer is validated before accessing protected endpoints, you need to implement a custom JWT verification function. This function will check the issuer (iss) claim in the token and ensure it matches an expected value. Here's how you can do this:

1. Define a custom callback function for JWT verification that checks the issuer.
2. Register this callback with the JWTManager.
3. Use this custom verification in the protected endpoints.

Here's the updated code with these changes:

```python
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token, verify_jwt_in_request
from functools import wraps

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random, secure key in production
app.config['JWT_IDENTITY_CLAIM'] = 'sub'  # This is the default, setting it for clarity
expected_issuer = 'your-issuer'  # Set your expected issuer here

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
            access_token = create_access_token(identity=username, additional_claims={"iss": expected_issuer})
            return jsonify(access_token=access_token), 200

    return jsonify({"msg": "The username or password is not correct"}), 401

def check_issuer():
    verify_jwt_in_request()
    jwt_token = request.headers.get('Authorization').split()[1]
    decoded_token = decode_token(jwt_token)
    issuer = decoded_token.get('iss')
    if issuer != expected_issuer:
        return jsonify({"msg": "Invalid issuer"}), 400

def issuer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        response = check_issuer()
        if response:
            return response
        return fn(*args, **kwargs)
    return wrapper

# Protected endpoint
@app.route('/user', methods=['GET'])
@jwt_required()
@issuer_required
def get_user():
    user_now = get_jwt_identity()
    return jsonify(logged_in_as=user_now), 200

@app.route('/languages', methods=['POST'])
@jwt_required()
@issuer_required
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
@issuer_required
def get_languages():
    user_now = get_jwt_identity()
    for user in users:
        if user.username == user_now:
            return jsonify(languages=user.get_languages())

# New protected endpoint to check issuer directly
@app.route('/check_issuer', methods=['GET'])
@jwt_required()
@issuer_required
def check_issuer_route():
    return jsonify({"msg": "Issuer is valid"}), 200

if __name__ == '__main__':
    app.run(debug=True)
```

In this updated code, the `issuer_required` decorator checks the issuer in the JWT token before allowing access to the protected endpoints. This ensures that the JWT issuer is validated properly.