#!/usr/bin/env python3
'''a Module to handle Authentication'''


from typing import List, TypeVar
from flask import request


class Auth:
    '''class to manage the API authentication.'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''check if a path requires authentication'''
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
        ''' '''
        return None
