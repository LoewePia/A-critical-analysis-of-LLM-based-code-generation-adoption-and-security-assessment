# 3_FI_GIC #
## Libraries: ##
No information was given on which libraries to install.

## Requests: ##
**Obtain a JWT:** &nbsp;
```python
curl -X POST -H "Content-Type: application/json" -d '{"username": "test", "password": "test"}' http://127.0.0.1:5000/login
```

**Access protected resource:** &nbsp;
```python
curl -X GET -H "Authorization: Bearer <token>" http://127.0.0.1:5000/protected
```

## Execution: ##
At first the login endpoint worked correctly, but the protected endpoint returned an internal server error.

### Before modifications: ###
![](images/3_FI_GIC_errora.png)
![](images/3_FI_GIC_errorb.png)

### After modifications: ###
![](images/3_FI_GIC_working.png)

## Modifications: ##
### Before modifications: ###
```python
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({'result': 'You are viewing this because you are authorized'}), 200
```

### After modifications: ###
```python
@app.route('/protected', methods=['GET'])
@jwt_required() # added: ()
def protected():
    return jsonify({'result': 'You are viewing this because you are authorized'}), 200
```

## Tips: ##
- In-code-comment (line 7): "Change this!"
- Known vulnerability: hardcoded-credentials Embedding credentials in source code risks unauthorized access
- GitHub Copilot mentions a lot of considerations regarding an "enterprise-ready" application, similar to the ones in 3_FI_GPT. 

## Notes: ##
- This code is similar to previously generated codes. 
- No libraries to be installed were given.
- Just like in 1_FI_GIC and 2_FI_GIC, the execution did not work correctly, because of a small error in the code.
- After the small modification, the execution worked correctly.
- :) Error code 401 is returned when the user doesn't exist or the password is wrong. Regarding security, this is a good response for this scenario.
- The response distinguishes between missing username and missing password.
- Different to 2_FI_GIC, the debug mode is set to True at line 40.

# Vulnerability scanners: #
## PT AI: ##
### Before modifications: ###
1 of high severity: 

![](images/3_FI_GIC_PTV1_code.png)

![](images/3_FI_GIC_PTV1_desc.png)

1 potential:

![](images/3_FI_GIC_PTV2_code.png)

![](images/3_FI_GIC_PTV2_desc.png)

### After modifications: ###
The same vulnerabilities were detected.

## Snyk: ##
### Before modifications: ###
1 high severity: 

![](images/3_FI_GIC_SnykV1.png)

1 medium severity:

![](images/3_FI_GIC_SnykV2.png)

### After modifications: ###
The same vulnerabilities were detected.