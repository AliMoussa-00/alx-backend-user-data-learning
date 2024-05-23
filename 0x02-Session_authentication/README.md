# Session authentication

[tasks](https://drive.google.com/file/d/1U16dhi1fzKGMhsbvqJHeVQ656CnzAp7p/view?usp=drive_link)

Simple HTTP API for playing with `User` model.

## Files

### `models/`

- `base.py`: base of all models of the API - handle serialization to file
  
- `user.py`: user model
  

### `api/v1`

- `app.py`: entry point of the API
  
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
  
- `views/users.py`: all users endpoints
  

## Setup

```
$ pip3 install -r requirements.txt
```

## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```

## Routes

- `GET /api/v1/status`: returns the status of the API
  
- `GET /api/v1/stats`: returns some stats of the API
  
- `GET /api/v1/users`: returns the list of users
  
- `GET /api/v1/users/:id`: returns an user based on the ID
  
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
  
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
  
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)
  

---

### What is a Cookie?

A **cookie** is a small piece of data sent from a website and stored on the user's computer by their web browser while they are browsing. Cookies are designed to be a reliable mechanism for websites to remember stateful information or to record the user's browsing activity.

### How Cookies Work

1. **Server Sets a Cookie**:
  
  - When a user visits a website, the server can send a cookie to the user's browser through the HTTP response header.
  - The browser stores this cookie and sends it back to the server with each subsequent request to the same domain.
  
  ```http
  HTTP/1.1 200 OK
  Set-Cookie: session_id=unique_session_id; HttpOnly; Path=/
  ```
  
2. **Browser Stores and Sends Cookie**:
  
  - The browser stores the cookie and automatically includes it in the HTTP request header when the user makes requests to the same domain.
  
  ```http
  GET /protected-resource
  Cookie: session_id=unique_session_id
  ```
  

### Components of a Cookie

- **Name**: The name of the cookie.
- **Value**: The value of the cookie.
- **Domain**: The domain for which the cookie is valid. The browser will send the cookie to this domain and all its subdomains.
- **Path**: The URL path that must exist in the requested URL for the browser to send the cookie.
- **Expiration Date**: When the cookie expires and is deleted. If not set, the cookie is a session cookie and will be deleted when the browser is closed.
- **Secure**: Indicates that the cookie should only be sent over secure (HTTPS) connections.
- **HttpOnly**: Indicates that the cookie is inaccessible via JavaScript (helps prevent cross-site scripting (XSS) attacks).

### Role of Cookies in Session-Based Authentication

In session-based authentication, cookies play a critical role in maintaining the authentication state between the client and server. Here’s how:

1. **User Logs In**:
  
  - User submits login credentials to the server.
  - Server verifies credentials and creates a session.
  - Server sends back a session ID as a cookie to the client.
2. **Client Stores Cookie**:
  
  - The client's browser stores the session ID cookie.
3. **Subsequent Requests**:
  
  - For each subsequent request, the browser automatically includes the session ID cookie.
  - Server validates the session ID to authenticate the user.
4. **User Logs Out**:
  
  - User requests to log out.
  - Server invalidates the session and optionally instructs the browser to delete the session cookie.

### Example in Flask

Here’s an example demonstrating how cookies are used in session-based authentication in Flask:

```python
from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# In-memory user store for demonstration purposes
users = {'user': 'pass'}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username in users and users[username] == password:
        session['username'] = username
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/protected-resource', methods=['GET'])
def protected_resource():
    if 'username' in session:
        return jsonify({'message': 'This is a protected resource', 'user': session['username']}), 200
    return jsonify({'message': 'Unauthorized'}), 401

if __name__ == '__main__':
    app.run()
```

### Security Considerations

- **Secure Flag**: Always set the `Secure` flag on cookies to ensure they are only sent over HTTPS.
- **HttpOnly Flag**: Set the `HttpOnly` flag to prevent access to cookies via JavaScript, mitigating XSS attacks.
- **SameSite Attribute**: Use the `SameSite` attribute to prevent CSRF attacks by restricting how cookies are sent with cross-site requests.

```http
Set-Cookie: session_id=unique_session_id; HttpOnly; Secure; SameSite=Strict
```

### Summary

Cookies are a fundamental part of web applications, used extensively for session management, personalization, and tracking. In session-based authentication, cookies help maintain user authentication state by storing session IDs and automatically including them in subsequent requests. Proper security measures, such as setting `HttpOnly`, `Secure`, and `SameSite` attributes, are crucial to protect cookies from common web vulnerabilities.

---

### How Session ID is Sent Back to the Frontend

Flask, the session ID is sent back to the frontend automatically when you set data in the `session` object. This is managed by Flask's built-in session handling mechanism. Here’s how it works in detail:

1. **Setting Session Data**:
  When you assign values to the `session` object, Flask knows that it needs to send a session cookie back to the client. For example, in the login route, we store the username in the session:
  
  ```python
  session['username'] = username
  ```
  
2. **Sending the Session Cookie**:
  After setting session data, Flask automatically generates a session ID, stores it in the server-side session store (which by default is a secure cookie), and sends it to the client in the `Set-Cookie` header of the HTTP response. The session ID is embedded within this cookie.
  
3. **Client Receives and Stores the Cookie**:
  The client's browser receives this cookie and stores it. The browser then automatically includes this cookie in the `Cookie` header of every subsequent request to the server.
  

### Example of the Process

Here’s a step-by-step example showing how this works using the previously provided Flask application:

1. **User Logs In**:
  
  - The client sends a POST request with login credentials.
  - Flask verifies the credentials and sets a session variable.
  
  ```python
  @app.route('/login', methods=['POST'])
  def login():
      data = request.json
      username = data.get('username')
      password = data.get('password')
      if username in users and users[username] == password:
          session['username'] = username  # Setting session data
          return jsonify({'message': 'Logged in successfully'}), 200
      return jsonify({'message': 'Invalid credentials'}), 401
  ```
  
2. **Flask Generates and Sends the Session Cookie**:
  
  - After setting `session['username']`, Flask generates a session ID.
  - The session ID is sent to the client as a cookie in the `Set-Cookie` header.
  
  ```http
  HTTP/1.1 200 OK
  Set-Cookie: session=<session_id>; HttpOnly; Path=/
  Content-Type: application/json
  
  {
      "message": "Logged in successfully"
  }
  ```
  
3. **Client Stores the Session Cookie**:
  
  - The client’s browser stores the session cookie.
  - For subsequent requests, the browser automatically includes this cookie.
4. **Client Makes Authenticated Request**:
  
  - The client makes a request to a protected resource.
  - The browser includes the session cookie in the request.
  
  ```http
  GET /protected-resource
  Cookie: session=<session_id>
  ```
  
5. **Flask Validates the Session**:
  
  - Flask reads the session cookie, validates the session ID, and retrieves the session data.
  - If the session is valid, Flask processes the request; otherwise, it returns an unauthorized response.
  
  ```python
  @app.route('/protected-resource', methods=['GET'])
  def protected_resource():
      if 'username' in session:
          return jsonify({'message': 'This is a protected resource', 'user': session['username']}), 200
      return jsonify({'message': 'Unauthorized'}), 401
  ```
  

### Conclusion

The process of sending the session ID to the frontend and including it in subsequent requests is handled automatically by Flask's session management system. When you set values in the `session` object, Flask generates a session ID, stores it in a secure cookie, and sends this cookie to the client. The client’s browser then automatically includes this session cookie in future requests, allowing Flask to maintain session state between requests.

This seamless handling makes session management in Flask straightforward, without requiring explicit management of the session ID in your application code.
