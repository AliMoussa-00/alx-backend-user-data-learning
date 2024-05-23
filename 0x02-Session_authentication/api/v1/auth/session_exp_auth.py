#!/usr/bin/env python3
'''session expiration Module'''


from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    '''class to implement expiration date for session id'''

    def __init__(self):
        '''Initializing the instance'''
        self.session_duration = 0

        try:
            duration = os.getenv('SESSION_DURATION', None)
            if duration:
                self.session_duration = int(duration)
        except ValueError:
            pass

    def create_session(self, user_id=None):
        '''
        create a session instance
        store the session_id
        the value of the session_id the stored: user_id and current datetime
        '''

        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {
            "user_id": user_id, "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''get the user for the session id'''
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id, None)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at', None)
        if created_at is None:
            return None

        expiration = created_at + timedelta(seconds=self.session_duration)
        if expiration < datetime.now():  # if expiration date is passed
            return None

        return session_dict.get('user_id')
