---
created: 2022-12-10
title: "Web token based authentication with JWT"
description: "What is JWT and how to use it to authenticate your API/Service users. . ."
layout: post
tags: [JWT, Python]
category: [Backend]
image:
  path: /assets/img/blogs/grad4-thumbnail.png
---

<br>
<div align="center">

بسم الله الرحمن الرحيم <br> احييكم بتحية الإسلام السلام عليكم ورحمة الله تعالى وبركاته

</div>
<br>

Hello world, Hossam is here, welcome to my 4th blog in the Graduation Project Diary series, in this blog I try to explain and discuss new things that I have learned during the final year @ BFCAI ❤️.

By the end of this post you will be able to tell the deference between the `Authentication` and `Authorization`, and what is the JWT, Why we need it, How does it work, and How we can use it protect APIs resources or endpoints.

# Introduction

JWT is important in authenticating user that using our API (Application Programming Interface) to protect your endpoints and verify that the request sender has the permission to perform that request. lets start by taking about the Authentication and Authorization

# Authentication and Authorization

Authentication and Authorization are two important concepts which always we can see someone get confusion with them and mix them together. so lets differentiate between them.

## What is Authentication

`Authentication` in brief **Is a process that verifies that someone is who they say they are.** It's like what we do when we try to login on Twitter for example and we provide a username and password, in this case the server takes our credentials and validate if them are correct to make us logging in correctly or push an error message.

## What is Authorization

`Authorization` in brief **is the security process that determines a user or service's level of access.** we use Authorization to check the users permissions.

## Two different techniques of authentication

We have two popular ways of authentication that `Session` based and `Token` based
in each one of them we use a deferent technique for authenticating the user/ request sender. in this post I'll use and discuss the token based approach.

### Session Based Authentication

in the session based approach we use the `session Id` to authorize the user. The user send the credentials and then the server send the session id in the browser cookies.
the image below [4] describe the process of authenticate user with session approach:

![Pasted image 20221210062823](https://user-images.githubusercontent.com/60070427/206869726-6219d1f1-80e1-4d8f-a151-b42d148a4c67.png)

### Token Based Authentication

In the session based approach the user/client send the credentials to the server, then the server generate a Token with secret key known only for the Server side and send back the token to the client.

when the client try to access server resources with the token, the server verify that token with the secret key and make sure that the token still valid and not expired. The image [4] below describe the process:

![Pasted image 20221210063253](https://user-images.githubusercontent.com/60070427/206869757-fc31015c-b474-4ebc-a9c2-254b6a52367c.png)

The Images above coped from [educative.io - Why should you use JWT's?](https://www.educative.io/answers/why-should-you-use-jwts)

## JWT or Sessions what should i choose?

In the session based approach, the server must store the session's data to authorize the user when he try to interact with the server again, but what about if we have to communicate with another server? in this case all servers must have a copy of sessions to authorized the user request when it's sent.

In the token case, server don't need to store the token. also the token can be user in multiple servers without running into problems where one server has a certain session, and the other server doesn’t.

modern web applications use the Token approach for authentication reasons like scalability and mobile device authentication.

# JSON Web Tokens (JWT)

## What is JWTs?

```
JWT (JSON Web Tokens) are an open, industry standard [RFC 7519] method for representing claims securely between two parties.
```

JWT makes it easy for the receiver to validate that the token received contains all of the information encoded by the issuer unmodified and as intended.

**JWT Example:**

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4iLCJuYW1lIjoiSG9zc2FtIEhhbWR5In0.zEhTPvYvQSe-7FVxFjpDLlkWoGoxsSVrBp65hDCSL8U
```

## What is JWT Consist of?

JWT consists of 3 parts of strings separated by a dot (.) symbol. this three parts are

1. **Header**
2. **Payload**
3. **Signature.**

### Header

JWT header consists of token `type` and `algorithm` used for signing and encoding.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload

JWT Payload is also a JSON object that contains the required data to verify the user identity, role, and permissions. An Example of JWT payload:

```json
{
  "role": "admin",
  "name": "Hossam Hamdy"
}
```

each field of the JSON key is called a `Claim`, the server used this claims such as `role` to verify that the user with the admin have the permissions to perform the action they are requesting.

Of course you are free to name your claims but here are some of the the standard claims that we can use such as:

1.  Issuer(iss)
2.  Subject (sub)
3.  Audience (aud)
4.  Expiration time (exp)
5.  Issued at (iat)

It's Important to be careful with claims, so don't put sensitive information in them because **JWT can be decoded easily**.

### Signature

The **signature** is the most important part that ensures that the token hasn’t been altered. To create the signature, the Base64-encoded header and payload are taken, along with a `secret`, and signed with the algorithm specified in the header.

```
HMACSHA512(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret
)
```

in our case we will create a private key known only for our end and use it in signing the JWTs that we will creates to validate the incoming tokens signatures and verify it's expiration time.

# How it Works

- The user try to authenticate with the `API-Key`
- The Server receive this information from the user then generate a JWT and sign them with it's secret key. and send the token to the user again.
- The user will send the token in the next request to access the server resources.
- The Server will receive the request and it'll start validation the token to check it's signature if true it will perform the action and response to the user, if not it'll returns error message.

# Using JWT with Python Flask

Lets creating flask API such that simple one we create in the last post. lets start with two simple endpoints that returns string messages. I'll implement simple flask API that have only two endpoints `home`, `secret`.

**Code**

```python
import json
from functools import wraps
import jwt
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/v3/home", methods=["GET"])
def home() -> str:
	return "hello world"

@app.route("/api/v3/secret", methods=["GET"])
def secret() -> str:
	return "Ops, it's sensitive data :("

def run_api(debug_mode: bool = True):
    app.run(debug=debug_mode)

if __name__ == '__main__':
    run_api(debug_mode=True)
```

if we test this code we will find that the user can access any end point of them, what if we want to restrict the `/secret` to the authenticated users only? that is what I'm writing this post for.

lets implement `auth` endpoint to make user ask for a token.

**Implement auth endpoint**

```python
API_KEY = "ABCDE"
SECRET_KEY = "MY-SECRET-TEXT"

@app.route("/api/v3/auth", methods=["GET"])
def api_auth():
    """Generate the jwt auth token for the front end team members"""
    # Reading data from request body
    req_data = request.data.decode()
    # getting the api-key
    key = json.loads(req_data)["api-key"]
    # Check if the key is correct
    if key == API_KEY:
	    # Generate the JWT response
        jwt_response = generate_jwt(SECRET_KEY)
        return jwt_response
    elif key != API_KEY:
        return {"data": {"message": "invalid api key", "code": 400}}
```

The `auth` end point handling GET requests at the `/api/v3/auth` path, it's receive the `api-key` from the user which is shared and check if it's correct then call the function called `generate_jwt` to handle the JWT generation we will see it's implementation after few seconds. otherwise return the `invalid api key` message.

**generate_jwt()**

```python
import jwt
import datetime

def generate_jwt(secret: str) -> dict:
    # after 3 minutes from now the jwt will be expired
    expiration_time = datetime.datetime.utcnow()+datetime.timedelta(minutes=3)
    # create jwt
    token = jwt.encode({"user":"front-team", "exp": expiration_time}, secret)
    return {
        "data": {
            "code": 200,
            "message": "Your token is created successfully",
            "token": f"{token}",
            "expiration_at": f"{expiration_time}"
        }
    }
```

in this function we take `secret` parameter which we will use in signing the the token as i mentioned earlier. then it calculate the expiration date and time, in this example i make it expire after 3 minutes from invocation time. after that we go to the most important part.

```python
token = jwt.encode({"user":"front-team", "exp": expiration_time}, secret)
```

in this line we encode the `payload` JSON and sign it with the secret value. after JWT generation it'll return the response to the user looks like that:

```json
{
  "data": {
    "code": 200,
    "message": "Your token is created successfully",
    "token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4iLCJuYW1lIjoiSG9zc2FtIEhhbWR5In0.SLzlGLkziGgyraprl69i-aSBHVI2WlkQEzs02qtKKs-NwX3l5dWKLHl_7hbCCnSQhiFroeCRkRrHzSQrYQbEqA",
    "expiration_at": "Date Time"
  }
}
```

now we are going to make the token required when requesting protected resources.

## Require the token to validate requests

```python
from functools import wraps
import jwt
import json
from flask import Flask, request, jsonify

def token_required(func):
    """Function to validate the passed token in the HTTP request"""

    @wraps(func)
    def decorated(*args, **kwargs):
        payload = request.data
        if len(payload) == 0:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        else:
            token = json.loads(payload)
            if "token" in token.keys():
                my_token = token["token"]
            else:
                return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            # Token is valid and can access the endpoint
            data = jwt.decode(my_token, SECRET_KEY, algorithms=['HS256'])
            # Don't do anything here.
            # That will make the request pass to the wrapped path

        except Exception as error_message:
            # We Have error here
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated
```

if it's your first time to see function wrap in python here is a useful resource for it [Function Wrappers in Python](https://www.codespeedy.com/function-wrappers-in-python/). In this code samples we wrap the `decorated` function that holds the authentication logic, with this technique we can annotate any function in our application with `@token_required` to validate the the passed token before performing the request operations. it's start by getting the `token` from the request body and then check for three probabilities:

1. The token it empty: in this case the API will return `Token is missing!` message.
2. The token is invalid: in this case the API will return `Invalid token` message.
3. The Token is valid passed: in this case we will try to decode the passed token as we see in the following line:
   ```python
   data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
   ```

we pass the token and the secret key which we encode the token with to validate the signature, and finally we pass the hashing algorithm that we used in JWT header.
if this decode process fails it's raise an exception which will response with the `Invalid token` at the previous point.

## Put them altogether

```python
import json
import jwt
from functools import wraps
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)
SECRET_KEY = "My-Secret-Key"

def generate_jwt(secret: str) -> dict:
    # after 3 minutes
    expiration_time = datetime.datetime.utcnow()+datetime.timedelta(minutes=3)
    # create jwt
    token = jwt.encode({"user": "Taro-Team", "exp": expiration_time}, secret)
    return {
        "data": {
            "code": 200,
            "message": "Your token is created successfully",
            "token": f"{token}",
            "expiration_at": f"{expiration_time}"
        }
    }


def token_required(func):
    """Function to validate the passed token in the HTTP request"""

    @wraps(func)
    def decorated(*args, **kwargs):
        payload = request.data
        if len(payload) == 0:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        else:
            token = json.loads(payload)
            if "token" in token.keys():
                my_token = token["token"]
            else:
                return jsonify({'Alert!': 'Token is missing!'}), 401
        try:
            # Token is valid and can access the endpoint
            data = jwt.decode(my_token, SECRET_KEY, algorithms=['HS256'])
            # Don't do anything here.
            # That will make the request pass to the wrapped path

        except Exception as error_message:
            # We Have error here
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


@app.route("/api/v3/auth", methods=["GET"])
def api_auth():
    """Generate the jwt auth token for the front end team members"""
    # Reading data from request body
    req_data = request.data.decode()
    key = json.loads(req_data)["api-key"]
    if key == API_KEY:
        jwt_response = generate_jwt(SECRET_KEY)
        return jwt_response
    elif key != API_KEY:
        return {"data": {"message": "invalid api key", "code": 400}}

@app.route("/api/v3/home", methods=["GET"])
def home() -> str:
    return "hello world"


@app.route("/api/v3/secret", methods=["GET"])
def secret() -> str:
    return "Ops, it's sensitive data :("


def run_api(debug_mode: bool = True):
    app.run(debug=debug_mode)  


if __name__ == '__main__':
    run_api(debug_mode=True)
```

Now, lets try to access `/secret` endpoint with postman like the image below:

![Pasted image 20221210190648](https://user-images.githubusercontent.com/60070427/206869788-83e6bac2-fbcd-4bd2-b66f-64c858ad9637.png)

as you can see nothing happened we still can access the `/secret` endpoint, that happened because we didn't add the `@token_required` annotation above the `secret` endpoint such as the following line:

```python
@token_required
@app.route("/api/v3/secret", methods=["GET"])
def secret() -> str:
    return "Opps, it's sensitive data :("
```

lets try again and check if we can access this anymore.

![Pasted image 20221210192955](https://user-images.githubusercontent.com/60070427/206869813-dfa20053-3b62-4e64-9c70-62cc42277cd8.png)

we can't access this endpoint without providing the token, now lets try to generate an API token by the `/auth` endpoint. as e mentioned earlier we need to provide the API Key to be able to get the JWT so I'll send this data in the request

```json
{
  "api-key": "testKey"
}
```

![Pasted image 20221210194739](https://user-images.githubusercontent.com/60070427/206869836-7b2c307d-6fcf-4a31-a3b3-266d804ab118.png)

After sending the API we get our token which is valid for 3 minuets only, then we send that token again with the request body to access the `/secret` endpoint as the image below and as we can see it's working as we want.

![Pasted image 20221210194821](https://user-images.githubusercontent.com/60070427/206869872-24ca6d1c-d202-4011-911d-dfa25ede3d66.png)

Now, lets try the last experiment. I waited for more that 3 minutes to test this case and validate that the JWT was expired and we will see how does it's automatically performed in our implementation.

![Pasted image 20221210200212](https://user-images.githubusercontent.com/60070427/206869893-5e2bbc6e-6cd7-494c-829f-e861d2ab8b9a.png)

As you can see, the token is invalid :).

# Conclusion

At the end of this post lets do a quick recap of what we covered, we talked about what is the deference between authentication and authorization, and we talk about authentications approaches such as sessions and web tokens. then we talk about The JWT (JSON Web Token) and how it's looks like and it's work for authentication. Then we implement the `/auth` endpoint to demonstrate the concept and testing it by accessing protected endpoints with the generated JWT.

I hope it was informative for you and Thank you for reading 💙

---

# Resources

- [jwt.io](https://jwt.io/)
- [The RFC Series](https://www.rfc-editor.org/rfc/rfc7519)
- [Token](https://en.wikipedia.org/wiki/Token)
- [How JWT (JSON Web Token) authentication works?](https://dev.to/t/webdev)
- [Encoding](https://www.techopedia.com/definition/948/encoding)
- [JSON Web Token Structure](https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-structure)
- [4- Why should you use JWT's?](https://www.educative.io/answers/why-should-you-use-jwts)
