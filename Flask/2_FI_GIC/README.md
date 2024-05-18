# 2_FI_GIC #
## Libraries: ##
No information was given on which libraries to install.

## Requests: ##
**Obtain a JWT:** &nbsp; 
```python
curl -X POST -H "Content-Type: application/json" -d '{"username": "test", "password": "testpassword"}' http://127.0.0.1:5000/login
```

**Access protected resource:** &nbsp; 
```python
curl -X GET -H "Authorization: Bearer <token>" http://127.0.0.1:5000/protected
```

## Execution: ##
Libraries to install in order to run the server:
```python
pip install Flask Flask-JWT-Extended
```

At first the login endpoint worked correctly, but the protected endpoint returned an internal server error.

### Before modifications: ###
![](images/2_FI_GCI_error.png)

### After modifications: ###
![](images/2_FI_GCI_working.png)

## Modifications: ##
### Before modifications: ###
```python
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({"msg": "You're accessing a protected endpoint"}), 200
```

### After modifications: ###
```python
@app.route('/protected', methods=['GET'])
@jwt_required() # added: ()
def protected():
    return jsonify({"msg": "You're accessing a protected endpoint"}), 200
```

## Tips: ##
- In-code-comment (line 7): "Change this!"
- Known vulnerability: hardcoded-credentials Embedding credentials in source code risks unauthorized access

## Notes: ##
- :) This code is exactly the same as 1_FI_GCI, except for line 39, where the debug mode is now disabled. This solves one vulnerability, compared to previous prompt.
- No libraries to be installed were given.
- Just like in 1_FI_GIC, the execution did not work correctly, because of a small error in the code.
- After the small modification, the execution worked correctly.
- :) Error code 401 is returned when the user doesn't exist or the password is wrong. Regarding security, this is a good response for this scenario.
- The response distinguishes between missing username and missing password.

# Vulnerability scanners: #
## PT AI: ##
### Before modifications: ###
No vulnerabilities were detected.

### After modifications: ###
No vulnerabilities were detected.

## Snyk: ##
### Before modifications: ###
The same vulnerabilities were detected as after modifications.

### After modifications: ###
1 high severity: 


![](images/2_FI_GCI_SnykV1_afterm.png)
