#!/usr/bin/env python3
"""
Main file
testing all the endpoint APIs
"""


import requests

BASE_URL = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    '''
    testing the creation of the user API
    API: /user  Method: POST
    '''
    url = f'{BASE_URL}/users'
    data = {'email': email, 'password': password}

    re = requests.post(url=url, data=data)

    assert re.status_code == 200
    assert re.json() == {"email": email, "message": "user created"}

    # if the user already registered
    re_invalid = requests.post(url=url, data=data)
    assert re_invalid.status_code == 400
    assert re_invalid.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    '''test login user with wrong password'''

    url = f'{BASE_URL}/sessions'
    data = {'email': email, 'password': password}

    re = requests.post(url=url, data=data)

    assert re.status_code == 401


def profile_unlogged() -> None:
    '''testing trying to access profile without being logged in'''

    url = f'{BASE_URL}/profile'
    cookies = {'session_id': None}

    re = requests.get(url=url, cookies=cookies)

    assert re.status_code == 403


def log_in(email: str, password: str) -> str:
    '''test login user with valid credentials'''

    url = f'{BASE_URL}/sessions'
    data = {'email': email, 'password': password}

    re = requests.post(url=url, data=data)

    assert re.status_code == 200
    assert re.json() == {"email": email, "message": "logged in"}
    assert 'session_id' in re.cookies

    return re.cookies.get('session_id')


def profile_logged(session_id: str) -> None:
    '''test accessing the profile of a logged in user'''
    url = f'{BASE_URL}/profile'
    cookies = {'session_id': session_id}

    re = requests.get(url=url, cookies=cookies)

    assert re.status_code == 200
    assert re.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    '''testing logout'''

    url = f'{BASE_URL}/sessions'
    cookies = {'session_id': session_id}
    re = requests.delete(url=url, cookies=cookies, allow_redirects=True)

    assert re.status_code == 200


def reset_password_token(email: str) -> str:
    '''test resetting password'''
    url = f'{BASE_URL}/reset_password'
    data = {'email': email}

    re = requests.post(url=url, data=data)

    assert re.status_code == 200

    token = re.json().get('reset_token')
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''test updating password'''
    url = f'{BASE_URL}/update_password'
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password}

    re = requests.put(url=url, data=data)

    assert re.status_code == 200
    assert re.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
