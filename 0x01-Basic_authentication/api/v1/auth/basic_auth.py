#!/usr/bin/env python3
'''Basic auth Module'''


import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    '''Implementing basic authentication'''

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        '''
        extract the authorization from header
        Return:
            - the Base64 part of the Authorization header
            for a Basic Authentication
        '''

        if authorization_header and type(authorization_header) == str:
            if authorization_header.startswith('Basic '):
                return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''
        returns the decoded value of a Base64 string of authorization header
        '''
        if base64_authorization_header and \
                type(base64_authorization_header) == str:
            try:
                decoded_bytes = base64.b64decode(base64_authorization_header)
                decoded_str = decoded_bytes.decode()
                return decoded_str

            except Exception:
                return None

        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''
        returns the user email and password from the Base64 decoded value.
        '''
        if decoded_base64_authorization_header and \
                type(decoded_base64_authorization_header) == str and \
                ':' in decoded_base64_authorization_header:

            email, pwd = decoded_base64_authorization_header.split(':', 1)

            return (email, pwd)

        return None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''
        returns the User instance based on his email and password.
        '''
        if not user_email or type(user_email) != str:
            return None
        if not user_pwd or type(user_pwd) != str:
            return None

        try:
            users = User.search({'email': user_email})

            for user in users:
                if user.is_valid_password(user_pwd):
                    return user

        except KeyError:
            return None

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        overloads Auth and retrieves the User instance for a request
        '''
        user = None

        authorization = self.authorization_header(request)

        base64_authorization = \
            self.extract_base64_authorization_header(authorization)

        decoded_authorization = \
            self.decode_base64_authorization_header(base64_authorization)

        credentials = self.extract_user_credentials(decoded_authorization)
        if credentials:
            user = self.user_object_from_credentials(
                credentials[0], credentials[1])

        return user
