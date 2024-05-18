from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_caching import Cache
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random, secure key in production
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 60

cache = Cache(app)
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

# Rate limiting function
def rate_limit(key, limit, period):
    current_time = datetime.now()
    request_times = cache.get(key) or []

    # Remove timestamps older than the period
    request_times = [t for t in request_times if current_time - t < timedelta(seconds=period)]

    if len(request_times) < limit:
        request_times.append(current_time)
        cache.set(key, request_times)
        return True
    else:
        return False

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
    rate_limit_key = f"{user_now}_add_language"

    if not rate_limit(rate_limit_key, limit=2, period=60):
        return jsonify({"msg": "Rate limit exceeded: You can only add a language 2 times per minute."}), 429

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