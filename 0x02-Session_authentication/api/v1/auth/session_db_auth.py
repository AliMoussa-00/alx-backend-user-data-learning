#!/usr/bin/env python3
'''Sessions in database'''


from datetime import datetime, timedelta

from flask import request
from api.v1.auth.session_exp_auth import SessionExpAuth
from models import user_session
from models.base import DATA
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    '''storing session ids in DB'''

    def __init__(self):
        '''Initializing the instance'''
        super().__init__()
        self.user_session = UserSession()

    def create_session(self, user_id=None):
        '''creating a session and storing session Id in DB'''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_session.user_id = user_id
        self.user_session.session_id = session_id

        self.user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''
        returns the User ID by requesting UserSession in
        the database based on session_id
        '''
        # get user sessions from DB (file)
        self.user_session.load_from_file()

        # get the user_session object based on session id
        users_sessions = self.user_session.search(
            {'session_id': session_id})

        if users_sessions == []:
            return None

        user_session = users_sessions[0]
        self.user_id_by_session_id[session_id] = user_session.user_id

        expiration = user_session.created_at + \
            timedelta(seconds=self.session_duration)
        if expiration < datetime.now():  # if expiration date is passed
            self.destroy_session(request)
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        '''remove session from db'''
        session_id = self.session_cookie(request)
        if session_id:

            users_sessions = self.user_session.search(
                {'session_id': session_id})

            if users_sessions != []:
                user_session = users_sessions[0]
                user_session.remove()
