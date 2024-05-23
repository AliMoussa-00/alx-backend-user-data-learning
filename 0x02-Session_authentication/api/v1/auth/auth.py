#!/usr/bin/env python3
'''a Module to handle Authentication'''


import os
from typing import List, TypeVar
from flask import request


class Auth:
    '''class to manage the API authentication.'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''check if a path requires authentication
        Return:
            - True: if path require authentication
            - False: if path does not require authentication
        '''
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True

        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:

            if excluded_path.find('*') != -1:
                index = excluded_path.find('*')
                if path[:index] == excluded_path[:index]:
                    return False

            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        '''return the value of the authorization header'''
        if request is None or \
                request.headers.get('Authorization', None) is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        ''' To override
        get the current user, based on the authentication type
        '''
        return None

    def session_cookie(self, request=None):
        '''returns a cookie value from a request'''
        if request is None:
            return None

        _my_session_id = os.getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
