#!/usr/bin/env python3
""" Module of session authentication views
"""

import os
from flask import jsonify, make_response, request
from api.v1.views import app_views
from models.user import User


@app_views.route(
    '/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user() -> str:
    """ POST /auth_session/login/
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - Set session id to cookies
      - 400 missing credentials
      - 404 invalid email
      - 401 invalid password for given email
    """
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({'error': 'email missing'}), 400
    if password is None or password == '':
        return jsonify({'error': 'password missing'}), 400

    users = User.search({'email': email})
    if users == []:
        return jsonify({'error': 'no user found for this email'}), 404

    current_user = None
    for user in users:
        if user.is_valid_password(password):
            current_user = user
            break

    if current_user is None:
        return jsonify({'error': 'wrong password'}), 401

    session_id = auth.create_session(current_user.id)
    response = make_response(jsonify(current_user.to_json()))

    session_name = os.getenv('SESSION_NAME')
    if session_name:
        response.set_cookie(session_name, session_id)

    return response
