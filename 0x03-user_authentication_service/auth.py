#!/usr/bin/env python3
'''Defining the Auth file'''


from typing import Optional
import uuid
import bcrypt

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    '''
    hashing a password
    parameters:
        - password: the user password as a string
    Return:
        - the hashed password as bytes
    '''

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    '''generate a unique UUID'''

    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
        create a User object and save it in the database,
        if the user already exists raise ValueError,
        save the user with the hashed password
        parameters:
            - email: email of the user
            - password: the plain text of the password
        Return:
            - the created user object
        '''

        if self._db.find_user_by(email=email):
            # user already exists
            raise ValueError(f'User {email} already exists')

        password = _hash_password(password)

        user = self._db.add_user(email, password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        '''
        check if the user is valid, by checking if email exists for a user,
        and the hashed password equals the user password
        parameters:
            - email: email of the user
            - password: the user's password
        Return:
            - True: if valid user
            - False: if not a valid user
        '''
        user = self._db.find_user_by(email=email)
        if user:
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True

        return False

    def create_session(self, email: str) -> str:
        '''
        create a unique session ID
        parameters:
            - email: the email to create a session for
        Return:
            - session_id as a string
        '''
        user = self._db.find_user_by(email=email)
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)

            return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        '''
        get the user with the corresponding session id
        parameters:
            - session_id: the session id
        Return:
            - the user instance
            - None, if no user found for the session_id
        '''
        if session_id:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        return None

    def destroy_session(self, user_id: int) -> None:
        '''
        destroy the session of a user by setting the user session_id to None
        parameters:
            - user_id: the user id to destroy its session
        Return: None
        '''
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        '''
        generate a reset password token for the user, and update the user's
        reset_token attribute.
        if the email does not belong to a user raise ValueError
        parameters:
            - email: email string of the user
        Return:
            - the generated reset password token as a string
        '''
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError('no user found for the passed email')

        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        '''
        reset the password for the user with reset_token value passed
        if the token does not belong to a user a ValueError will be raised
        parameters:
            - reset_token: to search for the user with this token
            - password: the new password for the user
        Return: None
        '''

        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError('no user found for the passed reset_token')

        self._db.update_user(user.id,
                             hashed_password=_hash_password(password),
                             reset_token=None)
