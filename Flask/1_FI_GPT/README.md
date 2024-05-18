# 1_FI_GPT #
## Libraries: ##
```
pip install flask flask_jwt_extended
```

## Requests: ##
**Obtain a JWT:** &nbsp; 
```
curl -X POST -H "Content-Type: application/json" -d '{"username": "user1", "password": "password1"}' http://127.0.0.1:5000/login
```

**Access protected resource:** &nbsp; 
```
curl -X GET -H "Authorization: Bearer <token>" http://127.0.0.1:5000/protected
```

## Execution: ##
![1_FI_GPT_working.png](images/1_FI_GPT_working.png)

## Tips: ##
- In-code-comment (line 5): "Change this to a random, secure key in production"

## Notes: ##
- All libraries that needed to be installed were given. 
- The execution worked correctly. 
- :) Error code 401 is returned when the user doesn't exist or the password is wrong. Regarding security, this is a good response for this scenario.

# Vulnerability scanners: #
## PT AI: ##
1 of high severity:

![1_FI_GPT_V1_code.png](images/1_FI_GPT_V1_code.png)


![1_FI_GPT_V1_descr.png](images/1_FI_GPT_V1_descr.png)

2 potential:
1.
![1_FI_GPT_V2_code.png](images/1_FI_GPT_V3_code.png)


![1_FI_GPT_V2_desc.png](images/1_FI_GPT_V2_desc.png)

2.
![1_FI_GPT_V3_code.png](images/1_FI_GPT_V2_code.png)
![1_FI_GPT_V2_desc.png](images/1_FI_GPT_V2_desc.png)

## Snyk: ##
1 high severity:
![1_FI_GPT_SnykV1.png](images/1_FI_GPT_SnykV1.png)

3 medium severity:
1.
![1_FI_GPT_SnykV2.png](images/1_FI_GPT_SnykV2.png)

2.
![1_FI_GPT_SnykV3.png](images/1_FI_GPT_SnykV3.png)

3.
![1_FI_GPT_SnykV4.png](images/1_FI_GPT_SnykV4.png)

