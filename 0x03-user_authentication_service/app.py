#!/usr/bin/env python3
'''Flask app file'''


from flask import Flask, abort, jsonify, make_response, redirect, request

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def main_route() -> str:
    '''main route API'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    '''create a user and save it in the DB'''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({
            "email": email,
            "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    '''
    login a valid user and create a session
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            re = make_response(
                jsonify({"email": email, "message": "logged in"}))

            re.set_cookie('session_id', session_id)
            return re
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    '''
    logout the user and destroy the session
    '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(session_id)
        return redirect('/')

    abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    '''access the user profile, using the session id'''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200

    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    '''return the reset_password token if the email is valid'''
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)

        return jsonify(
            {"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route('/update_password', methods=['PUT'])
def update_password() -> str:
    '''update the password for the user'''
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)

        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
